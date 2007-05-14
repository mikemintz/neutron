#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron module
#  adhoc.py

#  Copyright (C) 2006-2007 Grégoire Menuel <gregoire.menuel@gmail.com>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
sys.path.insert(1, 'modules')

import xmpp
from xmpp.protocol import *
import mod

class AdhocError(Exception):
  pass

class CommandHandler(xmpp.commands.Command_Handler_Prototype):

  typList=['fixed','boolean','hidden','jid-multi', 'jid-single', 'list-multi', 'list-single','text-multi','text-private','text-single']
  typList=['fixed','boolean','hidden','text-single','list-multi','list-single']
  
  def __init__(self,name,description,completeCB,data=None, dataFun=None):
    """ Init internal constants. """
    if data is None and dataFun is None:
      raise ArgumentError, "data ou dataFun ne doit pas être None"
    self.data=data
    self.dataFun=dataFun
    xmpp.commands.Command_Handler_Prototype.__init__(self)
    self.initial = {'execute':self.cmd}
    self.name=name
    self.completeCB=completeCB
    self.description=description

  def getData(self,jid=None):
    """Récupère les données, appelle dataFun ou utilise data"""
    if self.dataFun is not None:
      return self.dataFun(jid)
    return self.data

  def allowedType(self,typ):
    return typ in self.typList

  def convertSendType(self,value,typ):
    if typ=='boolean':
      if not type(value)==bool:
        raise AdhocError, "Valeur '"+value+"' incorecte pour le type '"+str(typ)
      return str(value).lower()
    else:
      return value

  def convertRecvType(self,value,typ):
    if typ=='boolean':
      if value=='1' or value.lower()=='true':
        return True
      elif value=='0' or value.lower()=='false':
        return False
      else:
        raise AdhocError, "Bad value '"+value+"' for type boolean"
    else:
      return value

  def getFields(self,jid=None):
    """Convertit une liste de la forme :
    [ {'name':"champ1", 'typ':"type champ 1", 'label':"label champ 1", 'desc': 'description', 'value':'valuer du champ'},
      {'name':'champ2'...},
    ]"""
    fields=[]
    dataList=self.getData(jid)
    for data in dataList:
      if type(data)==unicode or type(data)==str:
        #C'est juste un label
        fields.append(data)
      elif type(data)==dict:
        if not data.has_key('typ'):
          raise AdhocError, "A field must have a type"
        if not self.allowedType(data['typ']):
          raise AdhocError, "Not allowed type : "+data['typ']
        if data.has_key("value"):
          #on duplique les données pour ne pas modifier les données de base
          dat=data.copy()
          dat['value']=self.convertSendType(dat['value'],dat['typ'])
        else:
          dat=data
        fields.append(DataField(**dat))
        
      else:
        raise AdhocError, "The data isn't composed of unicode or dict"
    return fields

  def cmd(self,conn,request):
    """ Determine """
    # This is the only place this should be repeated as all other stages should have SessionIDs
    try:
      session = request.getTagAttr('command','sessionid')
    except:
      session = None
    if session == None:
      session = self.getSessionID()
      self.sessions[session]={'jid':request.getFrom(),'actions':{'cancel':self.cmdCancel,'complete':self.cmdComplete,'execute':self.cmdComplete},'data':{'type':None}}
      reply = request.buildReply('result')
      jid= request.getFrom().getStripped()
      form = DataForm(title=self.description, data=self.getFields(jid))
      replypayload = [Node('actions',attrs={'execute':'complete'},payload=[Node('complete')]),form]
      reply.addChild(name='command',attrs={'xmlns':NS_COMMANDS,'node':request.getTagAttr('command','node'),'sessionid':session,'status':'executing'},payload=replypayload)
      self._owner.send(reply)
      raise NodeProcessed

  def cmdComplete(self,conn,request):
    form = DataForm(node = request.getTag(name='command').getTag(name='x',namespace=NS_DATA))
    try:
      wiki = form.getField('wiki').getValue()
      away = form.getField('away').getValue()
      offline = form.getField('offline').getValue()
      busy = form.getField('busy').getValue()
    except:
      #pas normal que ca soit pas bon, surement un gus qui s'amuse pour voir si le script est résistant
      return
    jid=request.getFrom().getStripped()
    fields=form.getFields()
    fields_str={}
    try:
      for nam in fields.keys():
        if nam is None:
          continue
        fields_str[nam.encode('utf8')]=self.convertRecvType(fields[nam].getValue(),fields[nam].getType())
      if self.completeCB is not None:
        comp=self.completeCB(jid,**fields_str)
      else:
        comp=False
    except AdhocError:
      comp=False
    if comp:
      reply = request.buildReply('result')
      form = DataForm(typ='result',data=['Modifications prise en compte'])
      reply.addChild(name='command',attrs={'xmlns':xmpp.protocol.NS_COMMANDS,'node':request.getTagAttr('command','node'),'sessionid':request.getTagAttr('command','sessionid'),'status':'completed'},payload=[form])
    else:
      reply = Error(request,xmpp.ERR_BAD_REQUEST)
    self._owner.send(reply)
    raise NodeProcessed

  def cmdCancel(self,conn,request):
    reply = request.buildReply('result')
    reply.addChild(name='command',attrs={'xmlns':NS_COMMANDS,'node':request.getTagAttr('command','node'),'sessionid':request.getTagAttr('command','sessionid'),'status':'cancelled'})
    self._owner.send(reply)
    del self.sessions[request.getTagAttr('command','sessionid')]


class Mod(mod.Mod):
  """Adhoc est une classe permettant facilement d'utiliser des commandes ad-hoc pour configurer un plugin."""
  def __init__(self,glob):
    self.name="Adhoc"
    self.globals=glob
    self.version="0.1"
    self.commandList=[]
    self.commands=None

  def postConnexion(self):
    """Fonction exécutée après la connexion au serveur jabber"""
    self.commands=xmpp.commands.Commands(self.globals['BROWSER'])
    self.commands.PlugIn(self.globals['JCON'])
    pass
  
  def registerCommand(self,handler):
    self.commandList.append(handler)
    handler.plugin(self.commands)

  def unregisterCommand(self,handler):
    if handler in self.commandList:
      self.commandList.pop(handler)
      handler.plugout(self.commands)

  def getCommandHandler(self,*args, **kw):
    """Retourne un objet CommandHandler, voir la doc de cette classe"""
    return CommandHandler(*args,**kw)


