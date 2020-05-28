# ==============================================================================
# Copyright (c) 2020, Yamagishi Laboratory, National Institute of Informatics
# Original: https://github.com/mkotha/WaveRNN
# Modified: Yi Zhao (zhaoyi[at]nii.ac.jp)
# All rights reserved.
# ==============================================================================
import torch
import torch.nn as nn
import numpy as np
import utils.logger as logger

class UpsampleNetwork(nn.Module) :
    """
    Input: (N, C, L) numeric tensor

    Output: (N, C, L1) numeric tensor
    """
    def __init__(self, feat_dims, upsample_scales):
        super().__init__()
        self.up_layers = nn.ModuleList()
        self.scales = upsample_scales
        for scale in upsample_scales:
            conv = nn.Conv2d(1, 1,
                    kernel_size = (1, 2 * scale - 1))
            conv.bias.data.zero_()
            self.up_layers.append(conv)

    def forward(self, mels):

        n = mels.size(0)
        feat_dims = mels.size(1)
        x = mels.unsqueeze(1)
        for (scale, up) in zip(self.scales, self.up_layers):

            x = up(x.unsqueeze(-1).expand(-1, -1, -1, -1, scale).reshape(n, 1, feat_dims, -1))


        return x.squeeze(1)[:, :, 1:-1]

class UpsampleNetwork_F0(nn.Module) :
    """
    Input: (N, C, L) numeric tensor

    Output: (N, C, L1) numeric tensor
    """
    def __init__(self, upsample_scales):
        super().__init__()
        self.up_layers = nn.ModuleList()
        self.scales = upsample_scales
        for scale in upsample_scales:
            conv = nn.Conv2d(1, 1,
                    kernel_size = (1, 2 * scale - 1))
            conv.bias.data.zero_()
            self.up_layers.append(conv)

    def forward(self, f0):
        f0 = f0.unsqueeze(1)
        n = f0.size(0)
        f0_dims = f0.size(1)

        x = f0.unsqueeze(1)
        for (scale, up) in zip(self.scales, self.up_layers):

            x = up(x.unsqueeze(-1).expand(-1, -1, -1, -1, scale).reshape(n, 1, f0_dims, -1))

        x = x.squeeze(1)[:, :, 1:-1]
        x = x.squeeze(1)
        return x
