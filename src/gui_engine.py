#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import wx
from signature_matcher import SignatureMatcher

def init_list_ctrl(self):
    self.signature_estimation_result_list_ctrl.InsertColumn(0, u'ファイル名')
    self.signature_estimation_result_list_ctrl.InsertColumn(1, u'リンカバージョン推定')
    self.signature_estimation_result_list_ctrl.InsertColumn(2, u'文字列推定')

def on_file_ref_button_click(self):
    dialog = wx.FileDialog(None,
                           message=u'ファイルを選択',
                           defaultDir='',
                           defaultFile='',
                           wildcard='*.*',
                           style=wx.FD_OPEN)
    # dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        self.signature_estimation_object_text_ctrl.SetValue(dialog.GetPath())

def on_dir_ref_button_click(self):
    dialog = wx.DirDialog(None,
                          message=u'フォルダ選択',
                          defaultPath='',
                          style=wx.DD_DIR_MUST_EXIST)
    if dialog.ShowModal() == wx.ID_OK:
        self.signature_estimation_object_text_ctrl.SetValue(dialog.GetPath())
        
def on_exe_button_click(self):
    matcher = SignatureMatcher()
    
    path = self.signature_estimation_object_text_ctrl.GetValue()
    
    if os.path.isfile(path):
        result = matcher.estimate(path)
        line = os.path.basename(path)
        self.signature_estimation_result_list_ctrl.InsertStringItem(0, line)
        self.signature_estimation_result_list_ctrl.SetStringItem(0, 1, result[0])
        self.signature_estimation_result_list_ctrl.SetStringItem(0, 2, result[1])
    elif os.path.isdir(path):
        index = 0
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            result = matcher.estimate(file_path)
            line = file_name
            self.signature_estimation_result_list_ctrl.InsertStringItem(index, line)
            self.signature_estimation_result_list_ctrl.SetStringItem(index, 1, result[0])
            self.signature_estimation_result_list_ctrl.SetStringItem(index, 2, result[1])
            index += 1
            sys.stdout.flush()
