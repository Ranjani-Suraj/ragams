import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from os import sep
from audio_processing import *
import time
import math
import logging 

def differenceFunction_scipy(x, N, tau_max):
    """
    Compute difference function of data x. This corresponds to equation (6) in [1]
    Faster implementation of the difference function.
    The required calculation can be easily evaluated by Autocorrelation function or similarly by convolution.
    Wiener–Khinchin theorem allows computing the autocorrelation with two Fast Fourier transforms (FFT), with time complexity O(n log n).
    This function use an accellerated convolution function fftconvolve from Scipy package.
    :param x: audio data
    :param N: length of data
    :param tau_max: integration window size
    :return: difference function
    :rtype: list
    """
    x = np.array(x, np.float64)
    w = x.size
    x_cumsum = np.concatenate((np.array([0]), (x * x).cumsum()))
    conv = fftconvolve(x, x[::-1])
    tmp = x_cumsum[w:0:-1] + x_cumsum[w] - x_cumsum[:w] 
    tmp-= 2 * conv[w - 1:]
    return tmp[:tau_max + 1]


def differenceFunction(x, N, tau_max):
    """
    Compute difference function of data x. This corresponds to equation (6) in [1]
    Fastest implementation. Use the same approach than differenceFunction_scipy.
    This solution is implemented directly with Numpy fft.
    :param x: audio data
    :param N: length of data
    :param tau_max: integration window size
    :return: difference function
    :rtype: list
    """
    logging.info('differenceFunction')
    x = np.array(x, np.float64)
    logging.info(x)
    w = x.size
    logging.info(w)
    tau_max = min(tau_max, w)
    logging.info(tau_max)
    x_cumsum = np.concatenate((np.array([0]), (x * x).cumsum()))
    logging.info(x_cumsum)
    size = w + tau_max
    p2 = (size // 32).bit_length()
    logging.info(p2)
    nice_numbers = (16, 18, 20, 24, 25, 27, 30, 32)
    size_pad = min(x * 2 ** p2 for x in nice_numbers if x * 2 ** p2 >= size)
    logging.info(size_pad)
    fc = np.fft.rfft(x, size_pad)
    logging.info(fc)
    conv = np.fft.irfft(fc * fc.conjugate())[:tau_max]
    logging.info(conv)
    logging.info('...........')
    #logging.info(w:w - tau_max:-1)
    logging.info(w)
    #logging.info(:tau_max)
    logging.info(x_cumsum[w:w - tau_max:-1])
    logging.info(x_cumsum[w])
    logging.info(x_cumsum[:tau_max])
    logging.info(2 * conv)
    a = np.add(x_cumsum[w:w - tau_max:-1], x_cumsum[w], x_cumsum[:tau_max])
    return  a - 2* conv


def cumulativeMeanNormalizedDifferenceFunction(df, N):
    """
    Compute cumulative mean normalized difference function (CMND).
    This corresponds to equation (8) in [1]
    :param df: Difference function
    :param N: length of data
    :return: cumulative mean normalized difference function
    :rtype: list
    """

    cmndf = df[1:] * range(1, N) / np.cumsum(df[1:]).astype(float)  # scipy method
    return np.insert(cmndf, 0, 1)


def getPitch(cmdf, tau_min, tau_max, harmo_th=0.1):
    """
    Return fundamental period of a frame based on CMND function.
    :param cmdf: Cumulative Mean Normalized Difference function
    :param tau_min: minimum period for speechnn
    :param tau_max: maximum period for speech
    :param harmo_th: harmonicity threshold to determine if it is necessary to compute pitch frequency
    :return: fundamental period if there is values under threshold, 0 otherwise
    :rtype: float
    """
    tau = tau_min
    while tau < tau_max:
        if cmdf[tau] < harmo_th:
            while tau + 1 < tau_max and cmdf[tau + 1] < cmdf[tau]:
                tau += 1
            return tau
        tau += 1

    return 0  # if unvoiced


def compute_yin(sig, sr, dataFileName=None, w_len=512, w_step=256, f0_min=50.0, f0_max=4000.0, harmo_thresh=0.1):
    """
    Compute the Yin Algorithm. Return fundamental frequency and harmonic rate.
    :param sig: Audio signal (list of float)
    :param sr: sampling rate (int)
    :param w_len: size of the analysis window (samples)
    :param w_step: size of the lag between two consecutives windows (samples)
    :param f0_min: Minimum fundamental frequency that can be detected (hertz)
    :param f0_max: Maximum fundamental frequency that can be detected (hertz)
    :param harmo_tresh: Threshold of detection. The yalgorithmù return the first minimum of the CMND fubction below this treshold.
    :returns:
        * pitches: list of fundamental frequencies,
        * harmonic_rates: list of harmonic rate values for each fundamental frequency value (= confidence value)
        * argmins: minimums of the Cumulative Mean Normalized DifferenceFunction
        * times: list of time of each estimation
    :rtype: tuple
    """

    logging.info('Yin: compute yin algorithm')
    tau_min = int(sr / f0_max)
    tau_max = int(sr / f0_min)

    timeScale = range(0, len(sig) - w_len, w_step)  # time values for each analysis window
    times = [t / float(sr) for t in timeScale]
    frames = [sig[t:t + w_len] for t in timeScale]

    pitches = [0.0] * len(timeScale)
    harmonic_rates = [0.0] * len(timeScale)
    argmins = [0.0] * len(timeScale)

    for i, frame in enumerate(frames):

        # Compute YIN
        df = differenceFunction(frame, w_len, tau_max)
        cmdf = cumulativeMeanNormalizedDifferenceFunction(df, tau_max)
        p = getPitch(cmdf, tau_min, tau_max, harmo_thresh)

        # Get results
        if np.argmin(cmdf) > tau_min:
            argmins[i] = float(sr / np.argmin(cmdf))
        if p != 0:  # A pitch was found
            pitches[i] = float(sr / p)
            harmonic_rates[i] = cmdf[p]
        else:  # No pitch, but we compute a value of the harmonic rate
            harmonic_rates[i] = min(cmdf)

    if dataFileName is not None:
        np.savez(dataFileName, times=times, sr=sr, w_len=w_len, w_step=w_step, f0_min=f0_min, f0_max=f0_max,
                 harmo_thresh=harmo_thresh, pitches=pitches, harmonic_rates=harmonic_rates, argmins=argmins)
        logging.info('\t- Data file written in: ' + dataFileName)

    return pitches, harmonic_rates, argmins, times


def returnNotes(audioFileName, w_len=2202, w_step=1000, f0_min=150.0, f0_max=850.0, harmo_thresh=0.85,
         audioDir="C:\\work\\python-samples\\frequency-identification", dataFileName=None, verbose=4):
    """
    Run the computation of the Yin algorithm on a example file.
    Write the results (pitches, harmonic rates, parameters ) in a numpy file.
    :param audioFileName: name of the audio file
    :type audioFileName: str
    :param w_len: length of the window
    :type wLen: int
    :param wStep: length of the "hop" size
    :type wStep: int
    :param f0_min: minimum f0 in Hertz
    :type f0_min: float
    :param f0_max: maximum f0 in Hertz
    :type f0_max: float
    :param harmo_thresh: harmonic threshold
    :type harmo_thresh: float
    :param audioDir: path of the directory containing the audio file
    :type audioDir: str
    :param dataFileName: file name to output results
    :type dataFileName: str
    :param verbose: Outputs on the console : 0-> nothing, 1-> warning, 2 -> info, 3-> debug(all info), 4 -> plot + all info
    :type verbose: int
    """

    if audioDir is not None:
        audioFilePath = audioDir + sep + audioFileName
    else:
        audioFilePath = audioFileName


        

    logging.info("audioFilePath = " + audioFilePath)
    (sr, sig) = audio_read(audioFilePath, formatsox=False)
    logging.info(sr)
    logging.info(sig)

    start = time.time()
    pitches, harmonic_rates, argmins, times = compute_yin(sig, sr, dataFileName, w_len, w_step, f0_min, f0_max,
                                                          harmo_thresh)


    end = time.time()
    logging.info("Yin computed in: ", end - start)
    logging.info("pitches = ", pitches)
    duration = len(sig) / float(sr)

    if verbose > 3:
        # ax1 = plt.subplot(4, 1, 1)
        # ax1.plot([float(x) * duration / len(sig) for x in range(0, len(sig))], sig)
        # ax1.set_title('Audio data')
        # ax1.set_ylabel('Amplitude')
        # ax2 = plt.subplot(4, 1, 2)
        # ax2.plot([float(x) * duration / len(pitches) for x in range(0, len(pitches))], pitches)
        # ax2.set_title('F0')
        # ax2.set_ylabel('Frequency (Hz)')
        # ax3 = plt.subplot(4, 1, 3, sharex=ax2)
        # ax3.plot([float(x) * duration / len(harmonic_rates) for x in range(0, len(harmonic_rates))], harmonic_rates)
        # ax3.plot([float(x) * duration / len(harmonic_rates) for x in range(0, len(harmonic_rates))], [harmo_thresh] * len(harmonic_rates), 'r')
        # ax3.set_title('Harmonic rate')
        # ax3.set_ylabel('Rate')
        # ax4 = plt.subplot(4, 1, 4, sharex=ax2)
        # ax4.plot([float(x) * duration / len(argmins) for x in range(0, len(argmins))], argmins)
        # ax4.set_title('Index of minimums of CMND')
        # ax4.set_ylabel('Frequency (Hz)')
        # ax4.set_xlabel('Time (seconds)')
        # plt.show()

        pitches = [round(i, 2) for i in pitches]
        pitches = [round((12 * math.log((i / 440), 2) + 69)) for i in pitches]
        return pitches
