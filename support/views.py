from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Chat, ChatMessage, Ticket, Ticket_replay
from .forms import ChatMessageForm, TicketForm, TicketReplayForm


def admin_support(request):
    if request.user.is_superuser == True:
        chats = Chat.objects.all()
        context = {
            'chats': chats,
        }
        return render(request,'support/admin_support.html',context,)
    else:
        return render(request,'main/nsuper.html')


def admin_support_user(request, user):
    if request.user.is_superuser == True:
        author = User.objects.filter(username = user).first()
        Chat.objects.filter(name = author).update(read=True)
        chat = Chat.objects.filter(name = author).first()
        messages = ChatMessage.objects.filter(chat = chat)
        message_form = ChatMessageForm(request.POST)

        context = {
                "author":author,
                'messages': messages,
                'message_form': message_form,
            }

        return render(request,'support/admin_support_user.html',context,)
    else:
        return render(request,'main/nsuper.html')


def admin_post_message(request, user):
    if request.user.is_superuser == True:
        author = User.objects.filter(username = user).first()
        chat = Chat.objects.filter(name=author).first()
        message_form = ChatMessageForm(request.POST)
        if message_form.is_valid():
            message = ChatMessage.objects.create(
                    chat = chat,
                    name = request.user,
                    admin = True,
                    message = message_form['message'].value())
            message.save()
        return HttpResponseRedirect(reverse('support:admin_support_user', args=[author]))
    else:
        return render(request,'main/nsuper.html')


def customer_support(request):
    if request.user.is_authenticated == True:
        chat = Chat.objects.filter(name=request.user)

        if not chat:
            chat = Chat.objects.create(name=request.user)
            chat.save()
            return HttpResponseRedirect(reverse('support:customer_support'))

        else:
            chat = Chat.objects.filter(name = request.user).first()
            messages = ChatMessage.objects.filter(chat = chat)
            message_form = ChatMessageForm(request.POST)

            context = {
                'messages': messages,
                'message_form': message_form,
            }

            return render(request,'support/live_support.html',context,)
    else:
        return render(request,'main/nlogin.html')


def customer_post_message(request):
    if request.user.is_authenticated == True:
        Chat.objects.filter(name = request.user).update(read=False)
        chat = Chat.objects.filter(name=request.user).first()
        message_form = ChatMessageForm(request.POST)
        if message_form.is_valid():
            message = ChatMessage.objects.create(
                    chat = chat,
                    name = request.user,
                    message = message_form['message'].value())
            message.save()
        return HttpResponseRedirect(reverse('support:customer_support'))
    else:
        return render(request,'main/nlogin.html')


#conversations between admin and user.
def customer_ticket(request, c_id):
    if request.user.is_authenticated == True:
        tickets = Ticket.objects.filter(id=c_id)
        conversations = Ticket_replay.objects.filter(ticket_id=c_id)

        for ticket in tickets:
            ticket_title = ticket.sub_title
            ticket_description = ticket.sub_description
            ticket_state = ticket.state

        context = {
            'ticket_id': c_id,
            'ticket_title': ticket_title,
            'ticket_description': ticket_description,
            'ticket_state': ticket_state,
            'ticket_conversation': conversations,
        }

        return render(request,'support/support_ticket.html',context,)
    else:
        return render(request,'main/nlogin.html')

def create_ticket(request):
    if request.user.is_authenticated == True:
        return render(request,'support/create_ticket.html',)
    else:
        return render(request,'main/nlogin.html')


def customer_ticket_list(request):
    if request.user.is_authenticated == True:
        tickets = Ticket.objects.filter(name = request.user)

        context = {
            'tickets': tickets,
        }

        return render(request,'support/support_ticket_list.html',context,)
    else:
        return render(request,'main/nlogin.html')


def customer_post_ticket(request):
    if request.user.is_authenticated == True:
        ticket_form = TicketForm(request.POST)
        if ticket_form.is_valid():
            ticket = Ticket.objects.create(
                    name = request.user,
                    sub_title = ticket_form['sub_title'].value(),
                    sub_description=ticket_form['sub_description'].value())
            ticket.save()
        return HttpResponseRedirect(reverse('support:customer_ticket_list'))
    else:
        return render(request,'main/nlogin.html')

def support_list(request):
    if request.user.is_authenticated == True:
        return render(request, 'support/support_list.html')
    else:
        return render(request, 'main/nlogin.html')



def customer_ticket_replay(request):
    if request.user.is_authenticated == True:
        ticket_form = TicketReplayForm(request.POST)
        ticket = Ticket_replay.objects.create(
                sub_description=ticket_form['sub_description'].value(),
                ticket_id = ticket_form['ticket_id'].value(),)
        ticket.save()
        return HttpResponseRedirect(reverse('support:customer_ticket', args=(ticket_form['ticket_id'].value(),) ))
    else:
        return render(request,'main/nlogin.html')

def ticket_state_change(request, state, ticket_id):
    if request.user.is_authenticated == True:
        Ticket.objects.filter(id = ticket_id).update(state=state)
        return HttpResponseRedirect(reverse('support:customer_ticket_list'))
    else:
        return render(request,'main/nlogin.html')







