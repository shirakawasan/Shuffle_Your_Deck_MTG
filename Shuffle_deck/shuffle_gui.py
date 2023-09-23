import wx
from urllib.request import urlopen
from PIL import Image
import io
import sys

sys.path.append('../')
import shuffle_deck as sd

# event function
class GUI:
    def __init__(self):
        # path setting
        self.icon_path = r"Shuffle_deck/images/icon.png"
        
        # initializing Frame
        self.frame = wx.Frame(None, wx.ID_ANY, 'Shuffle Your Deck!', size=(1600,1000), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.MINIMIZE_BOX | wx.ICONIZE)
        self.frame.SetBackgroundColour('#2b2b2b')

        # icon setting
        self.icon = wx.Icon(self.icon_path, wx.BITMAP_TYPE_PNG)
        self.frame.SetIcon(self.icon)

        # Create status bar.
        self.frame.CreateStatusBar()

        # Setting Font
        self.textfont = wx.Font(17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        # Decklist input
        self.panel_decklist = wx.Panel(self.frame, wx.ID_ANY, pos=(0,0), size=(500,700))

        self.decklist_title = wx.StaticText(self.panel_decklist, wx.ID_ANY, 'MO Decklist', pos=(10,10))
        self.decklist_title.SetForegroundColour('#FFFFFF')
        self.decklist_title.SetFont(self.textfont)

        self.decklist_textinput = wx.TextCtrl(self.panel_decklist, wx.ID_ANY, style=wx.TE_MULTILINE,size=(400,600),pos=(50,50))
        self.decklist_textinput.SetBackgroundColour("#666666")

        self.decklist_inputbutton = wx.Button(self.panel_decklist, wx.ID_ANY, 'Inport Deck!', pos=(200,660))
        self.decklist_textinput.SetFont(self.textfont)
        self.decklist_inputbutton.Bind(wx.EVT_BUTTON, self.click_deckinput_button)


        # Shuffle result Display
        self.panel_result = wx.Panel(self.frame, wx.ID_ANY, pos=(500,0), size=(500,700))
        self.shuffle_textoutput = wx.TextCtrl(self.panel_result, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY,size=(400,600),pos=(50,50))
        self.shuffle_textoutput.SetBackgroundColour("#666666")
        self.shuffle_textoutput.SetFont(self.textfont)

        self.result_title = wx.StaticText(self.panel_result, wx.ID_ANY, 'Shuffle Result', pos=(10,10))
        self.result_title.SetForegroundColour('#FFFFFF')
        self.result_title.SetFont(self.textfont)


        # Shuffle button Panel
        self.panel_shufflebutton = wx.Panel(self.frame, wx.ID_ANY, pos=(1000,0), size=(600,700))
        

        # Deal Shuffle Button
        self.dealshufflepanel = wx.Panel(self.panel_shufflebutton, wx.ID_ANY, pos=(50,50), size=(200,200))
        self.dealshufflepanel.SetBackgroundColour("#88b388")

        self.dealtext_title = wx.StaticText(self.dealshufflepanel, wx.ID_ANY, 'Deal Shuffle', pos=(10,10))
        self.dealtext_title.SetFont(self.textfont)

        self.dealtext_pile = wx.StaticText(self.dealshufflepanel, wx.ID_ANY, 'Number of Pile', pos=(10,35))
        self.deal_pile_input = wx.TextCtrl(self.dealshufflepanel, wx.ID_ANY,style=wx.TE_RIGHT,size=(180,20),pos=(10,55))
        
        self.dealtext_check = wx.StaticText(self.dealshufflepanel, wx.ID_ANY, 'Random', pos=(10,75))
        self.dealcheck = wx.CheckBox(self.dealshufflepanel, wx.ID_ANY, pos=(80,90))

        self.dealbutton = wx.Button(self.dealshufflepanel, wx.ID_ANY, 'Shuffle', pos=(65,160))
        self.dealbutton.Bind(wx.EVT_BUTTON, self.click_deal_button)
        
        # Hindu Shuffle Button
        self.hindushufflepanel = wx.Panel(self.panel_shufflebutton, wx.ID_ANY, pos=(350,50), size=(200,200))
        self.hindushufflepanel.SetBackgroundColour("#d8bfd8")

        self.hindutext_title = wx.StaticText(self.hindushufflepanel, wx.ID_ANY, 'Hindu Shuffle', pos=(10,10))
        self.hindutext_title.SetFont(self.textfont)

        self.hindutext_time = wx.StaticText(self.hindushufflepanel, wx.ID_ANY, 'Number of Hindu Shuffle', pos=(10,35))
        self.hindu_time_input = wx.TextCtrl(self.hindushufflepanel, wx.ID_ANY,style=wx.TE_RIGHT,size=(180,20),pos=(10,55))
        

        self.hindubutton = wx.Button(self.hindushufflepanel, wx.ID_ANY, 'Shuffle', pos=(65,160))
        self.hindubutton.Bind(wx.EVT_BUTTON, self.click_hindu_button)

        # Reset Button
        self.resetpanel = wx.Panel(self.panel_shufflebutton, wx.ID_ANY, pos=(350,350), size=(200,200))
        self.resetpanel.SetBackgroundColour("#b0c4de")

        self.resettext_title = wx.StaticText(self.resetpanel, wx.ID_ANY, 'Reset', pos=(10,10))
        self.resettext_title.SetFont(self.textfont)

        self.resetbutton = wx.Button(self.resetpanel, wx.ID_ANY, 'Reset', pos=(65,160))
        self.resetbutton.Bind(wx.EVT_BUTTON, self.click_reset_button)

        # show initial hand
        self.panel_initialhand = wx.Panel(self.frame, wx.ID_ANY, pos=(0,700), size=(1600,300))

        # initializing deck
        self.deck = sd.Card_Deck()

    # input deck
    def click_deckinput_button(self,event):
        decklist_string = self.decklist_textinput.GetValue()
        # initialize deck
        self.deck = sd.Card_Deck()
        try:
            self.deck.deck_import(decklist_string)
        except ValueError as e:
            self.frame.SetStatusText('MO Decklist format may not have been entered correctly.')
            self.shuffle_textoutput.SetValue("")
            return None
        except IndexError as e:
            self.frame.SetStatusText('There may be a line break on the last line of input or a blank line in MO Decklist.')
            self.shuffle_textoutput.SetValue("")
            return None
        
        # display initial library
        self.shuffle_textoutput.SetValue(self.deck.make_display_string())
        # self.shuffle_textoutput.SetValue(decklist_string)
        self.frame.SetStatusText('Your Deck is imported!')
        return None
    
    # deal shuffle
    def click_deal_button(self,event):
        try:
            number_of_pile = int(self.deal_pile_input.GetValue())
        except ValueError as e:
            self.frame.SetStatusText('Enter the appropriate value in the space provided.')
            return None
        
        random_state = self.dealcheck.GetValue()
        if random_state == True:
            msg, success_flag = self.deck.shuffle_deal_random(self.deck.shuffledecklist,number_of_pile)
        elif random_state == False:
            msg, success_flag = self.deck.shuffle_deal_nonrandom(self.deck.shuffledecklist,number_of_pile)
        self.frame.SetStatusText(msg)
        if success_flag:
            self.shuffle_textoutput.SetValue(self.deck.make_display_string())
            self.show_initial_hand()
        else:
            pass
        return None
    
    def click_hindu_button(self,event):
        try:
            time = int(self.hindu_time_input.GetValue())
        except ValueError as e:
            self.frame.SetStatusText('Enter the appropriate value in the space provided.')
            return None
        
        msg, success_flag = self.deck.shuffle_deal_random(self.deck.shuffledecklist,time)
        if success_flag:
            self.shuffle_textoutput.SetValue(self.deck.make_display_string())
            self.show_initial_hand()
        else:
            pass
        self.frame.SetStatusText(msg)
        return None
    
    def click_reset_button(self,event):
        self.shuffle_textoutput.SetValue(self.deck.reset())
        return None
    
    def show_initial_hand(self):
        card_image_url_list = self.deck.make_initialhand_url()
        for i in range(7):
            card_image_url = card_image_url_list[i]
            file = io.BytesIO(urlopen(card_image_url).read())
            image = wx.Image(file)
            image.Rescale(150, 210)
            bitmap = image.ConvertToBitmap()
            position = (10+160*i,10)
            cardpanel = wx.Panel(self.panel_initialhand, wx.ID_ANY,size=(150,210),pos=position)
            bi = wx.StaticBitmap(cardpanel,-1,bitmap)

        return None
