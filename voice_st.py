import os
import pickle
import torch
import librosa
from synthesis import build_model
from synthesis import wavegen
import numpy as np
from math import ceil
from model_vc import Generator

class Voice_ST:

    def __init__(self):
        return None

    def __pad_seq__(self, x, base=32):

        len_out = int(base * ceil(float(x.shape[0]) / base))
        len_pad = len_out - x.shape[0]
        assert len_pad >= 0
        return np.pad(x, ((0, len_pad), (0, 0)), 'constant'), len_pad

    def __encode__(self, source, target):
        '''

        Produces result.pkl
        :param source: string of source filename
        :param target: string of target filename
        :return: None
        '''

        source = "audio/upload/p225.pkl"
        target = "audio/upload/p256.pkl"
        
        device = 'cuda:0'
        G = Generator(32, 256, 512, 32).eval() #.to(device)

        g_checkpoint = torch.load('autovc.ckpt', map_location=torch.device('cpu'))#, map_location='cuda:0')
        G.load_state_dict(g_checkpoint['model'])

        # load data
        source = pickle.load(open(source, "rb"))
        target = pickle.load(open(target, "rb"))

        metadata = [source, target]

        # do work
        spect_vc = []

        x_org = source[2]
        x_org, len_pad = self.__pad_seq__(x_org)
        uttr_org = torch.from_numpy(x_org[np.newaxis, :, :])#.to(device)
        emb_org = torch.from_numpy(source[1][np.newaxis, :])#.to(device)

        emb_trg = torch.from_numpy(target[1][np.newaxis, :])#.to(device)

        with torch.no_grad():
            _, x_identic_psnt, _ = G(uttr_org, emb_org, emb_trg)

        if len_pad == 0:
            uttr_trg = x_identic_psnt[0, 0, :, :].cpu().numpy()
        else:
            uttr_trg = x_identic_psnt[0, 0, :-len_pad, :].cpu().numpy()

        spect_vc.append(('{}x{}'.format(source[0], target[0]), uttr_trg))

        # save the result
        with open('results.pkl', 'wb') as handle:
            pickle.dump(spect_vc, handle)

        return None

    def __decode__(self):

        spect_vc = pickle.load(open('results.pkl', 'rb'))
        #device = torch.device("cuda")
        model = build_model()#.to(device)
        checkpoint = torch.load("checkpoint_step001000000_ema.pth", map_location=torch.device('cpu'))
        model.load_state_dict(checkpoint["state_dict"])

        for spect in spect_vc:
            name = spect[0]
            c = spect[1]
            print(name)
            waveform = wavegen(model, c=c)

            save_path = os.path.join("audio/download/audio.wav")
            librosa.output.write_wav(save_path, waveform, sr=16000)

        return save_path

    def run(self, source, target):
        self.__encode__(source, target)
        saved_file = self.__decode__()
        return saved_file
