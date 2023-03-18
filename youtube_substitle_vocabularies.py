#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 22:54:30 2021

@author: ngatran
"""
# version 3: use ScrolledText library.

import sys
import os
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import collections
from youtube_transcript_api import YouTubeTranscriptApi
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import scrolledtext 
# my classes
import textual_process as rtf 
from textual_process import * 

# Source: https://www.geeksforgeeks.org/python-downloading-captions-from-youtube/
def download_youtube_script(video_id):
## download substitle
  transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
  for transcript in transcript_list:
      d = transcript.translate('en').fetch()
      text_script = ''
      for s in d:
          text_script += ' ' + s['text'] 
      break
  return(text_script)

def ask_youtube_url():
## Create a window to ask about youtube link 
    root = tk.Tk()
    root.withdraw()
    message = 'Give me your Youtube link'
    youtube_url = simpledialog.askstring("Hello...", message)
    root.quit()
    # Destroy the main window and any child windows
    root.destroy()
    return(youtube_url)

#Source: https://www.geeksforgeeks.org/python-tkinter-scrolledtext-widget/
def save_known_words(word_list, filepath):
## Create a window shows wordlist with checkboxes, and 2 buttons to save known words and show new words 
    def save_to_file(): 
        ## Slice known words 
        # Get checkboxes state 
        checked = [checkvars[x].get() for x in range(n)]
        # Indexes of known words 
        index_kw = [i for i, x in enumerate(checked) if x == 1]        
        # Create a dataframe known words and save to excel file 
        df_wordlist = pd.DataFrame(word_list).iloc[index_kw,:]
        with pd.ExcelWriter(filepath,mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
            df_wordlist.to_excel(writer, sheet_name="Main", header=None
                                 , startrow=writer.sheets["Main"].max_row,index=False)
            
        ## Pop up message about number of known words
        message = '{} words are added to your file'.format(len(index_kw))
        tk.messagebox.showinfo('Cglt!', message)   
    
    def show_new_words():
        ## Slice new words
        checked = [checkvars[x].get() for x in range(n)]
        new_word_list = [word_list[i] for i, x in enumerate(checked) if x == 0]
        
        ## Create new listbox window to show new words
        root2 = tk.Tk()        
        root2.title("{} new words for today".format(len(new_word_list)))
        listbox = scrolledtext.ScrolledText(root2, width=50, height=50)
        # Insert items into the listbox
        for word in new_word_list:
            listbox.insert(tk.END, word + "\n")

        listbox.pack()
        root2.mainloop()
        root2.quit()
        
    ## Create a ScrolledText widget
    root = tk.Tk()
    root.title("Choose words you already know")
    text = scrolledtext.ScrolledText(root, width=50, height=50)
    text.pack()
    
    ## Create checkboxes from word list 
    # Checkbox variables 0/1
    checkvars = [] 
    n = len(word_list)
    for x in range(n):
        checkvars.append(tk.IntVar())
        cb = tk.Checkbutton(text, text=word_list[x], bg='white', anchor='w'
                            , variable=checkvars[x])
        text.window_create('end', window=cb)
        text.insert('end', '\n')
        
    ## Functional button to save known words
    bt = tk.Button(root, text="Save these words!", command = save_to_file)
    text.window_create('end', window=bt)
    text.insert('end', '\n')     
    # Functional button to show new words 
    bt2 = tk.Button(root, text="Here are your new words", command = show_new_words)
    text.window_create('end', window=bt2)
    text.insert('end', '\n')
                       
    root.mainloop()
    root.quit()

if __name__ == "__main__":
    # "Common Words" filepath
    filepath_cwds = './common_words.xlsx'
    
    ##### Step 1: Get youtube id
    youtube_url = ask_youtube_url()
    video_id = youtube_url[youtube_url.index("=")+1:]
    
    ##### Step 2: Generate text script
    text_script = download_youtube_script(video_id)
    
    ##### Step 3: Textual processing 
    text_script = text_script.lower()
    text_script = rtf.remove_useless_characters(text_script)
    word_list = text_script.split()
    word_list = rtf.remove_common_words(word_list)
    word_list = rtf.remove_meaningless_words(word_list)
    
    ##### Step 4: Interaction to devide new words and known words
    save_known_words(word_list, filepath_cwds)


