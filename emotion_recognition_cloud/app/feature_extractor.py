"""
MFCC Feature Extraction Module
Extracted from the Complete Emotion Recognition Pipeline notebook
"""

import numpy as np
import scipy.io.wavfile as wavfile
import scipy.fftpack as fourier
import scipy.signal as sg
import math


class MelFreqCepsCoef:
    """Custom MFCC Feature Extraction Class"""
    
    def __init__(self, file_name, n_mfcc=40, frame_length=0.03, overlap=50, n_filters=22):
        """Initialize MFCC feature extraction with custom parameters."""
        # Load audio file
        self.fs, self.signal = wavfile.read(file_name)
        
        # Parameters
        self.f_max = self.fs / 2.0
        self.preemphasis = 0.0
        self.frame = frame_length
        self.overlap = overlap
        self.window = 2  # Hann window
        self.f_min = 0
        self.n_filters = n_filters
        self.n_mfcc = n_mfcc
        self.norm = 1
        self.rasta = 0
        
        # Process audio
        self.audio = self.signal / 32767
        self.audio_length = len(self.signal)
        self.frame_size = np.fix(self.frame * self.fs)
        self.overlap_size = np.fix(self.frame_size - self.frame_size * (self.overlap / 100.0))
        self.n_frames = self.__Frames()
        self.audio_avg = self.__Stereo()
        self.half_n = np.fix(self.frame_size / 2.0)
        self.window_data = self.__Window()
        self.freqs = self.__Freqs()
        self.mel_freqs = self.__Mel_Freqs()
        self.mel_filter_bank = self.__Mel_Filter()
        self.coef, self.nl = self.__MFCC_Coef()
        self.coef = self.coef[:, 0:self.nl]
        self.mfccsscalade = np.mean(self.coef.T, axis=0)
    
    def __Stereo(self):
        """Convert stereo to mono and apply preemphasis."""
        n_channel = len(np.shape(self.audio))
        if n_channel > 1:
            temp_1 = self.audio[:, 0]
            temp_2 = self.audio[:, 1]
            avg = (temp_1 + temp_2) / 2
        else:
            avg = self.audio
        
        if self.preemphasis != 0.0:
            Avg = np.zeros(len(avg))
            Avg[0] = avg[0]
            for n in range(1, len(avg)):
                Avg[n] = avg[n] - self.preemphasis * avg[n-1]
            return Avg
        else:
            return avg
    
    def __Frames(self):
        """Determine number of frames."""
        i = 0
        j = 0
        while j < self.audio_length:
            j = i * self.overlap_size + self.frame_size
            i = i + 1
        return i - 1
    
    def __Window(self):
        """Apply window function."""
        n = np.arange(-self.half_n, self.half_n)
        if len(n) != self.frame_size:
            n = np.arange(-self.half_n, self.half_n + 1)
        
        if self.window == 0:  # Box window
            W = np.ones(len(n))
        elif self.window == 1:  # Hamming window
            a, b = 0.53836, 0.46164
            W = np.array([a + b * math.cos((2 * math.pi * i) / (self.frame_size - 1.0)) for i in n])
        elif self.window == 2:  # Hann window
            a, b = 0.5, 0.5
            W = np.array([a + b * math.cos((2 * math.pi * i) / (self.frame_size - 1.0)) for i in n])
        return W
    
    def __Freqs(self):
        """Calculate frequencies in Hz."""
        n = np.arange(0, self.half_n)
        return np.array([(i * self.fs) / self.frame_size for i in n])
    
    def __Mel_Freqs(self):
        """Calculate Mel frequencies."""
        n = np.arange(0, self.half_n)
        return np.array([2595 * np.log10(self.freqs[int(i)] / 700 + 1) for i in n])
    
    def __Mel_Filter(self):
        """Generate triangular filter bank."""
        phi_min = 2595 * math.log10(self.f_min / 700 + 1)
        phi_max = 2595 * math.log10(self.f_max / 700 + 1)
        dphi = (phi_max - phi_min) / (self.n_filters + 1)
        fc = np.zeros(self.n_filters + 2)
        fc[0] = self.f_min
        for i in range(1, len(fc)):
            phic = (i - 1) * dphi
            fc[i-1] = 700 * (math.pow(10, (phic + phi_min) / 2595) - 1)
        fc[self.n_filters + 1] = self.f_max
        
        Hkm = np.zeros((int(self.half_n), self.n_filters))
        n = np.arange(0, self.half_n)
        for i in range(1, self.n_filters + 1):
            for k in n:
                kk = int(k)
                if self.freqs[kk] < fc[i-1]:
                    Hkm[kk, i-1] = 0
                elif (self.freqs[kk] >= fc[i-1]) and (self.freqs[kk] < fc[i]):
                    Hkm[kk, i-1] = (self.freqs[kk] - fc[i-1]) / (fc[i] - fc[i-1])
                elif (self.freqs[kk] >= fc[i]) and (self.freqs[kk] < fc[i+1]):
                    Hkm[kk, i-1] = (self.freqs[kk] - fc[i+1]) / (fc[i] - fc[i+1])
                elif self.freqs[kk] >= fc[i+1]:
                    Hkm[kk, i-1] = 0
        return Hkm
    
    def __MFCC_Coef(self):
        """Calculate MFCC coefficients."""
        frame = np.zeros(int(self.frame_size))
        self.energy = np.zeros((int(self.half_n), self.n_frames))
        self.cepstrum = np.zeros((self.n_filters, self.n_frames))
        Xm = np.zeros(self.n_filters)
        mfcc = np.zeros(self.n_mfcc)
        wi = np.zeros(2 * self.n_mfcc)
        MFCC = np.zeros((self.n_mfcc, self.n_frames))
        
        # Liftering weights
        for i in range(0, 2 * self.n_mfcc):
            wi[i] = 1 + self.n_mfcc * np.sin(math.pi * i / (2 * self.n_mfcc - 1))
        
        # RASTA filter coefficients
        numer = np.arange(-2, 3)
        numer = -numer / np.sum(numer * numer)
        denom = np.array([1, -0.98])
        
        l = 0
        for i in range(0, int(self.n_frames)):
            frame = self.audio_avg[i*int(self.overlap_size):i*int(self.overlap_size)+int(self.frame_size)]
            
            # Autocorrelation function
            acorr = np.correlate(frame, frame, mode='full')
            m = np.amax(acorr[20:len(acorr)])
            
            if m > 0.1:
                frame = frame * self.window_data
                P = np.abs(fourier.fft(frame))
                self.energy[:, l] = 10 * np.log10(P[0:int(self.half_n)])
                
                for j in range(0, self.n_filters):
                    Ps = P[0:int(self.half_n)] * self.mel_filter_bank[:, j]
                    if self.rasta == 1:
                        Ps = np.log(1 + Ps)
                        Ps = sg.lfilter(numer, denom, Ps)
                        Ps = np.exp(Ps) - 1
                    Xm[j] = np.log(np.sum(Ps))
                
                self.cepstrum[:, l] = Xm
                
                # DCT
                for j in range(1, self.n_mfcc + 1):
                    suma = 0
                    for k in range(1, self.n_filters + 1):
                        suma += Xm[k-1] * np.cos(math.pi * j * (k - 0.5) / self.n_filters)
                    mfcc[j-1] = suma
                
                mfcc = mfcc * wi[0:self.n_mfcc]
                MFCC[:, l] = mfcc
                l = l + 1
        
        # Normalize
        if self.norm == 1:
            MFCC = (MFCC - np.mean(MFCC)) / np.std(MFCC)
        
        return MFCC, l

