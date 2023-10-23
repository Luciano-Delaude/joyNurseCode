#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:31:10 2018

@author: Luciano Delaude, Quiming Lei, Santiago Agudelo
"""

from numpy import *
import time
import speech_recognition as sr
from gtts import gTTS
#quiet the endless 'insecurerequest' warning
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
from pygame import mixer

from mutagen.mp3 import MP3
import ffmpeg
import os
import cv2


class Joy():

  def __init__(self):
    os.system("clear")
    mixer.init()
    self.welcome = False
    self.responseUser = []
    self.data = []
    self.cont = 0
    self.counter = 0
    self.Question = 0
    self.diseaseFlag = False

  def assistance(self):
    while (True == True):

      if (self.welcome == False):
        self.joySpeaks('Hello!, I am joy, your electronic nurse')
        self.welcome = True

      print('============================>')
      for i in range(0,3):
        while (i != self.cont):
          if (self.diseaseFlag == False):
              self.joySpeaks(self.illnessQuestion(self.cont))
              self.cont = self.comunicationJoyUser(self.cont)
              print('Self cont is: ', self.cont)
          if (self.cont == 9):
            self.analysis()
            break
            

  # play message 
  def joySpeaks(self,message):
    tts = gTTS(text=message, lang='en')
    tts.save("joy.mp3")
    mixer.music.load("joy.mp3")
    mixer.music.play()
    audio = MP3("joy.mp3")
    audioLength = audio.info.length  
    time.sleep(audioLength+1)

  # obtain audio from the microphone
  def userSpeaks(self):
    with sr.Microphone() as source:
      sr.Recognizer().adjust_for_ambient_noise(source, duration=1)
      os.system("clear")
      print("Joy listens you!")
      audio = sr.Recognizer().listen(source,phrase_time_limit=3)
      return audio

  def userValidation(self,audio):
    print(audio) 
    try:
      response = sr.Recognizer().recognize_google(audio)
      
      return response

    except sr.UnknownValueError:
      self.joySpeaks('sorry, I didn\'t understand you. Can you repeat please?')
    except sr.RequestError as e:
      print("Sphinx error; {0}".format(e))
      self.joySpeaks('sorry, I didn\'t understand you. Can you repeat please?')

  def illnessQuestion(self,ind):
    
    if ind == 0:
      message = 'for start, tell me your age'
    elif ind == 1:
      message = 'Now, we can continue, tell me one if you are Women or zero if you are Men'
    elif ind == 2:
      message = "Let's continue, on a scale of one to four, how much pain you feel in your chest, where one is a lot and four is not so much"
    elif ind == 3:
      message = "Great, now let's go with the parameters of the analyzer. First tell me the resting blood pressure a value between 94 and 200"
    elif ind == 4:
      message = "Second, tell me the serum cholestoral, again a value between 126 and 564"
    elif ind == 5:
      message = "Third, is your fasting blood sugar level greater than 120 mg/dl? Answer zero if yes or one if not."
    elif ind == 6:
      message = "Fourth, tell me the resting electrocardiographic results, valid answers zero, one and two" #VER QUE SIGNIFICA 0, 1 y 2
    elif ind == 7:
      message = "Fifth, which is your maximum heart rate achieved? valid answer a value between 71 and 202"
    elif ind == 8:
      message = "Sixth, do you have angina induced by exercise? Answer zero if yes or one if not"
    return message

  def is_number(self,s):
      try:
          float(s)
          return True
      except ValueError:
          pass
  
      try:
          import unicodedata
          unicodedata.numeric(s)
          return True
      except (TypeError, ValueError):
          pass
      return False

  def joyAnalizer(self,response,cont):
    validite = False

    if (self.is_number(response)):
      if(self.cont == 0 and (response >= '0')):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
      elif(self.cont == 1 and (response == '1' or response == '0')):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
      elif(self.cont == 2 and (response == '1' or response == '2' or response == '3' or response == '4')):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
      elif(self.cont == 3 and (float(response) >= 94) and (float(response) <= 200)):
        print('valid data saved')
        self.responseUser.append(float(response))
        self.bloodPresure()
        validite = True
      elif(self.cont == 4 and (float(response) >= 126) and (float(response) <= 564)):
        print('valid data saved')
        self.responseUser.append(float(response))
        self.CoronaryArteryAnomalyDisease(self.responseUser[4])
        validite = True
      elif(self.cont == 5 and (response == '1' or response == '0')):
        print('valid data saved')
        self.responseUser.append(float(response))
        self.FastingBloodSugar(self.responseUser[5])
        validite = True
      elif(self.cont == 6 and (response == '0' or response == '1' or response == '2')):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
      elif(self.cont == 7 and (float(response) >= 71) and (float(response) <= 202)):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
      elif(self.cont == 8 and (response == '1' or response == '0')):
        print('valid data saved')
        self.responseUser.append(float(response))
        validite = True
    else:
      self.joySpeaks('sorry maybe you made a mistake, let\'s try again with the last question!')
    return validite

  def joyUnderstood(self,response):
    und = False
    self.joySpeaks("I think you said '"+response+"'. It's that ok? Please answer yes or not")
    print("This understand Joy ",response)
    var = True
    while(var == True):
      print('...........')
      audio = self.userSpeaks()
      response2 = self.userValidation(audio)
      print("This understand Joy: ",response2)
      if (response2 != None):
        if (response2.find('Yes') != -1 or response2.find('yes') != -1 or response2.find('Yeah') != -1 or response2.find('yeah') != -1):
          und = True
          return und
        elif (response2.find('No') != -1 or response2.find('no') != -1 or response2.find('Not') != -1 or response2.find('not') != -1 ):
          self.joySpeaks('sorry I\'m still developing, let\'s try again!')
          var = False
        else:
          self.joySpeaks('Please answer yes or not?')
      else:
        self.joySpeaks('Please answer yes or not?')

  def comunicationJoyUser(self,cont):
    audio = self.userSpeaks()
    response = self.userValidation(audio)
    if (response != None):
      und = self.joyUnderstood(response)
      if (und == True):
        validite = self.joyAnalizer(response,self.cont)
        if (validite == True):
          cont += 1
    return cont

  def pretreatment(self):
    f = open('heart.txt', 'r')
    data = list()
    maxi_list = list()
    mini_list = list()
    for i in f.readlines():
        temp_list = i[:-1].split(' ')
        for j in range(len(temp_list)):
            temp_list[j] = float(temp_list[j])
        data.append(temp_list)

    data_stand = list()
    for i in range(len(data)):
        data_stand.append(list())
    for i in range(len(data[0])):
        colon = list()
        for j in range(len(data)):
            colon.append(data[j][i])
        maxi = max(colon)
        mini = min(colon)
        maxi_list.append(maxi)
        mini_list.append(mini)
        for x in range(len(colon)):
            colon[x] = (colon[x] - mini)/(maxi - mini)
            data_stand[x].append(colon[x])
    train_x = list()
    train_y = list()
    test_x = list()
    test_y = list()
    for x in data_stand[:200]:
        train_x.append(x[0:-1])
        train_y.append([x[-1]])
    for x in data_stand[200:]:
        test_x.append(x[0:-1])
        test_y.append([x[-1]])
    return train_x, train_y, test_x, test_y, maxi_list, mini_list


  def sigmoid(self,x):
      return 1.0 / (1 + exp(-x))

  def train_log_regres(self,train_x, train_y, opts):
      # Calculate training time
      start_time = time.time()

      num_samples, num_features = shape(train_x)
      alpha = opts['alpha']
      max_iter = opts['maxIter']
      weights = ones((num_features, 1))

      # Optimize through gradient descent algorithm
      for k in range(max_iter):
          if opts['optimizeType'] == 'gradDescent':
              output = self.sigmoid(mat(train_x) * mat(weights))
              error = train_y - output
              weights = weights + alpha * mat(train_x).transpose() * error
          elif opts['optimizeType'] == 'stocGradDescent':
              for i in range(num_samples):
                  output = self.sigmoid(train_x[i, :] * weights)
                  error = train_y[i, 0] - output
                  weights = weights + alpha * mat(train_x[i, :]).transpose() * error
          else:
              raise NameError('Not support optimize method type!')
      print('Training complete with %fs!' % (time.time() - start_time))
      return weights

  def test_log_regres(self,weights, test_x, test_y):
      num_samples, num_features = shape(test_x)
      match_count = 0
      for i in range(num_samples):
          predict = self.sigmoid(mat(test_x[i][:]) * mat(weights))[0][0] > 0.5
          if predict == bool(test_y[i][0]):
              match_count += 1
      accuracy = float(match_count) / num_samples
      return accuracy


  def analysis(self):
      print('step1: load data...')
      trainX, trainY, testX, testY, maxiList, miniList = self.pretreatment()

      print('step2: training...')
      opts = {'alpha': 0.01, 'maxIter': 20, 'optimizeType': 'gradDescent'}
      optimalWeights = self.train_log_regres(trainX, trainY, opts)

      print('step3: testing...')
      accuracy = self.test_log_regres(optimalWeights, testX, testY)
      print('Our prediction accuracy is: %.3f%%' % (accuracy * 100))

      print('Step4: Now let\'s apply:')
      print('Please input your information required:')
      para = list()
      for i in range(9):
          para.append((float(self.responseUser[i]) - miniList[i]) / (maxiList[i] - miniList[i]))
          print(para)
      possibility = self.sigmoid(mat(para) * mat(optimalWeights))[0][0]
      print('Your possibility for having heart problem is %.3f%%' % (possibility[0][0] * 100))
      return
      
 #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  def userVerifier(self, Question):
    audio = self.userSpeaks()
    response = self.userValidation(audio)
    if (response != None):
      und = self.joyUnderstood(response)
      if (response.find('Yes') != -1 or response.find('yes') != -1 or response.find('Yeah') != -1 or response.find('yeah') != -1):
          self.counter +=1
          print('Self.Counter is: ', self.counter)
      if(und == True):
          self.Question += 1
          self.joySpeaks('Okay, let me save that')

    return self.Question, self.counter
    
  def bloodPresure (self):
      
        blood_presure = self.responseUser[3] #NO RETORNA A PREGUNTAR LA MISMA PREGUNTA, QUIZAS DEBA HACERLO CON EL IND DE ILLNESQUESTION.....
        self.counter = 0
        if(blood_presure <= 120): 
            self.joySpeaks( 'You don\'t have disease related to blood pressure level')
        #Si es mayor que tal nivel, ver que sintomas me produce
            return
        if(blood_presure > 120): 
            self.joySpeaks('Okay, that\'s a high level, let me ask you some more questions')
            self.diseaseFlag = True   
            print('Disease Flag is :', self.diseaseFlag)
            for k in range(0,5):
              print ('K is ', k)
              while (k != self.Question):
                self.joySpeaks(self.bloodPresureQuestion(self.Question))
                self.Question, _ = self.userVerifier(self.Question)
                print(self.Question)
                
            if  self.Question == 4:
                if (self.counter == 3 or self.counter ==4):
                    self.joySpeaks('You might have Vascular disease, for this case you should see your doctor to be sure')
                    self.diseaseFlag = False
                    self.Question = 0
                else:
                    self.joySpeaks('You are okay')
                    self.diseaseFlag = False
                    self.Question = 0
                    return
            else:
                return
        
  def FastingBloodSugar (self, fasting_blood_sugar):
      self.counter = 0
      if (fasting_blood_sugar == 1):
            self.joySpeaks( 'You don\'t have disease related to fasting blood sugar level')          
      if(fasting_blood_sugar == 0):  
            self.joySpeaks('Okay, that could be a problem, let me ask you some more questions')
            self.diseaseFlag = True   
            print('Disease Flag is :', self.diseaseFlag)
            for k in range(0,4):
              print ('K is ', k)
              while (k != self.Question):
                self.joySpeaks(self.FastingBloodSugarQuestion(self.Question))
                self.Question, _ = self.userVerifier(self.Question)
                print(self.Question)
                
            if  self.Question == 3:
                if (self.counter == 2 or self.counter == 3):
                    self.joySpeaks('You probably have Diabetes, for a better diagnostic you should see your doctor')
                    self.diseaseFlag = False
                    self.Question = 0
                else:
                    self.joySpeaks('You are okay')
                    self.diseaseFlag = False
                    self.Question = 0
                    return
            else:
                return

        
  def CoronaryArteryAnomalyDisease(self, serum_cholesterol):
        self.counter = 0
        if(serum_cholesterol <= 250):
            self.joySpeaks( 'You don\'t have disease related to serum cholesterol level')
        if(serum_cholesterol > 250):
            self.joySpeaks('Okay, that\'s a high level, let me ask you some more questions')
            self.diseaseFlag = True   
            print('Disease Flag is :', self.diseaseFlag)
            for k in range(0,5):
              print ('K is ', k)
              while (k != self.Question):
                self.joySpeaks(self.CoronaryArteryAnomalyDiseaseQuestion(self.Question))
                self.Question, _ = self.userVerifier(self.Question)
                print(self.Question)
                
            if  self.Question == 4:
                if (self.counter == 3 or self.counter ==4):
                    self.joySpeaks('You might have coronary artery disease, for this case you should see your doctor to be sure')
                    self.diseaseFlag = False
                    self.Question = 0
                else:
                    self.joySpeaks('You are okay')
                    self.diseaseFlag = False
                    self.Question = 0
                    return
            else:
                return
        
  def bloodPresureQuestion(self,ind):
    
    if ind == 0:
      message = 'Question 1: Do you have chest pain?'
    elif ind == 1:
      message = 'Question 2: Do you feel leg cramps?'
    elif ind == 2:
      message = 'Question 3: Do you have exercise induced angina?'
    elif ind == 3:
      message = 'Question 4: Do you have warm skin?'
    return message

  def FastingBloodSugarQuestion(self,ind):
    
    if ind == 0:
      message = 'Question 1: Do you have exercise induced angina?'
    elif ind == 1:
      message = 'Question 2: Do you feel tremors? I mean, involuntary shaking of differents parts of your body'
    elif ind == 2:
      message = 'Question 3: Do you feel equilibration disorders? I want to sey, if you feel a disturbance when youre standing or walking?'

    return message
    
  def CoronaryArteryAnomalyDiseaseQuestion(self,ind):
    
    if ind == 0:
      message = 'Question1: Maybe you have abdominal pain?'
    elif ind == 1:
      message = 'Question 2: Maybe do you feel bloated and your skin is stretched and shiny?'
    elif ind == 2:
      message = 'Okay,now look at your hands and tell me if you see them trembling a little bit...'
    elif ind == 3:
      message = 'Finally do you feel disorders of equilibrium?'
    return message
    
joy = Joy()
joy.assistance()


