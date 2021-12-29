from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import Markdown
from . import util


class SearchForm(forms.Form):
    query = forms.CharField(label="search title")

class NewPage(forms.Form):
    Title = forms.CharField(label="enter the title of your page", max_length=20)
    paragraph = forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    Title = forms.CharField(label="enter the title of your page", max_length=20 )
    paragraph = forms.CharField(widget=forms.Textarea )

# Posting something new
def New_entry(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('Title')
            body = form.cleaned_data.get('paragraph')
            replica = False
            for titles in util.list_entries():
                if title == titles:
                    replica = True 
                    break          
            if replica == True:
                return render( request, "encyclopedia/Display.html", {"Title": "Error" , "content": "An entry with the same title already exists" })
            else:
                util.save_entry(title, body)
                form = NewPage()
                return render( request, "encyclopedia/Display.html", {"Title": title , "content": body })

    # if request is a get        
    else:
        createform = NewPage()
        return render(request, "encyclopedia/Newentry.html" , {"Form":createform })
   



# first page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries() , "form":SearchForm
    })

# showing the entries and titles on a new page
def display(request,title):
        #content = util.get_entry(title)
        content = util.get_entry(title)
        if content == None:
            error = " there is nothing for this entry"
            return render( request, "encyclopedia/Display.html", {"content": error  })
        else:
            form = SearchForm()
            return render( request, "encyclopedia/Display.html", {"Title": title , "content": content , "form":form })
    

#searching for an entry 
def search(request):
    Queryform = SearchForm()
    guesslist =[]     # a list for the things the user might have wanted to search                                        
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            present = False   
            #Check if the exact thing they entered if there
            for entries in util.list_entries():                     
                if query == entries:
                    Searchcontent = util.get_entry(entries)
                    present = True
                    return render(request, "encyclopedia/Display.html" , {"Title": query , "content":Searchcontent} )
                else:
                    # check if entered word is similar to others
                    for predictions in util.list_entries():                 
                        if query.upper() in predictions.upper():
                            Prediction = predictions
                            guesslist.append(predictions)
                            present = True
                            return render(request, "encyclopedia/Display.html" , {"Title": 'Where You looking for these ?' ,"Guesses": guesslist ,"form":Queryform} )    
            #IF there is nothing similar to a searche query
            if present == False:
                return render(request, "encyclopedia/Display.html" , {"Title": 'Nothing close was found' ,"form":Queryform})

    else:
        return render(request, "encyclopedia/layout.html"
        , {"form":Queryform })

        


# going to random pages
def Random(request):
    Allentries = util.list_entries()
    count = len(Allentries)
    select = random.randint(0,count -1)
    Allentries = util.list_entries()
    RandomEntry = Allentries[select]
    randomcontent = util.get_entry(RandomEntry)
    return render( request, "encyclopedia/Display.html", {"Title": RandomEntry , "content": randomcontent  })


       
# Edit an entry
def Edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('Title')
            body = form.cleaned_data.get('paragraph')
            util.save_entry(title, body)
            return render( request, "encyclopedia/Display.html", {"Title": title , "content": body })
    else:
        To_be_edited = util.get_entry(title)
        form = EditForm(initial={'paragraph': To_be_edited, 'Title':title})
        return render( request, "encyclopedia/Edit.html", {"Form": form ,"Title":title})
    
    
  

