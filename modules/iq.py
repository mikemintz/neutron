# -*- coding: koi8-r -*-
## OJAB iq module
## Copyright (C) Boris Kotov <admin@avoozl.ru>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

# Modified by me :) Gh0st AKA Bohdan Turkynewych
import os, xmpp, time

messages=None
global version
global vername
ver_queue={}
time_queue={}
iq_id=1

def versioncmd(conn, msg, args, replyto):
    if args=="":
        target=msg.getFrom()
    else:
        target=("%s/%s"%(replyto, args))
    req=xmpp.protocol.Iq('get', xmpp.NS_VERSION, {}, target)
    req.setID(iq_id)
    ver_queue[str(iq_id)]=[replyto, msg.getFrom().getResource(), False]
    conn.send(req)
    globals()['iq_id']+=1

def pingcmd(conn, msg, args, replyto):
    if args=="":
        target=msg.getFrom()
    else:
        target=("%s/%s"%(replyto, args))
    req=xmpp.protocol.Iq('get', xmpp.NS_VERSION, {}, target)
    req.setID(iq_id)
    ver_queue[str(iq_id)]=[replyto, msg.getFrom().getResource(), time.time()]
    conn.send(req)
    globals()['iq_id']+=1

def timecmd(conn, msg, args, replyto):
    if args=="":
        target=msg.getFrom()
    else:
        target=("%s/%s"%(replyto, args))
    req=xmpp.protocol.Iq('get', xmpp.NS_TIME, {}, target)
    req.setID(iq_id)
    time_queue[str(iq_id)]=[replyto, msg.getFrom().getResource()]
    conn.send(req)
    globals()['iq_id']+=1

def versionCB(conn, iq_obj):
    uname=os.popen("uname -sr", 'r')
    osver=uname.read().strip()
    uname.close()
    pipe = os.popen('sh -c ' + '"' + 'python -V 2>&1' + '"')
    python_ver = pipe.read(1024).strip()
    osver = osver + ' ' + python_ver
    iq_obj=iq_obj.buildReply('result')
    qp=iq_obj.getTag('query')
    qp.setTagData('name', vername)
    qp.setTagData('version', version)
    qp.setTagData('os', osver)
    conn.send(iq_obj)
    raise xmpp.NodeProcessed

def versionresultCB(conn, iq_obj):
    qp=iq_obj.getTag('query')
    rname=qp.getTagData('name')
    rversion=qp.getTagData('version')
    ros=qp.getTagData('os')
    rid=iq_obj.getID()
    if ver_queue.has_key(rid):
        if ver_queue[rid][2]:
            if ver_queue[rid][1]==iq_obj.getFrom().getResource():
                conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['yourping']%(ver_queue[rid][1], str(round(time.time()-ver_queue[rid][2],3))), 'groupchat'))
            else:
                conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['ping']%(ver_queue[rid][1], iq_obj.getFrom().getResource(), str(round(time.time()-ver_queue[rid][2],3))), 'groupchat'))
        else:
            if ver_queue[rid][1]==iq_obj.getFrom().getResource():
                conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['yourversion']%(ver_queue[rid][1], rname, rversion, ros), 'groupchat'))
            else:
                conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['version']%(ver_queue[rid][1], iq_obj.getFrom().getResource(), rname, rversion, ros), 'groupchat'))

def versionerrorCB(conn, iq_obj):
    rid=iq_obj.getID()
    if ver_queue.has_key(rid):
        if ver_queue[rid][2]:
            conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['ping_error']%(ver_queue[rid][1], iq_obj.getFrom().getResource()), 'groupchat'))
        else:
            conn.send(xmpp.protocol.Message(ver_queue[rid][0], messages['version_error']%(ver_queue[rid][1], iq_obj.getFrom().getResource()), 'groupchat'))

def timeCB(conn, iq_obj):
    timep=os.popen("date -u '+%Y%m%dT%T'", 'r'); futc=timep.read(17); timep.close()
    timep=os.popen("date '+%Z|%d/%m/%Y %T|'", 'r'); ftime=timep.read(); timep.close()
    iq_obj = iq_obj.buildReply('result')
    qp = iq_obj.getTag('query')
    qp.setTagData('utc', futc)
    qp.setTagData('tz', ftime.split("|")[0])
    qp.setTagData('display', ftime.split("|")[1])
    conn.send(iq_obj)
    raise xmpp.NodeProcessed

def timeresultCB(conn, iq_obj):
    qp=iq_obj.getTag('query')
    rdisplay=qp.getTagData('display')
    rid=iq_obj.getID()
    if time_queue.has_key(rid):
        if time_queue[rid][1]==iq_obj.getFrom().getResource():
            conn.send(xmpp.protocol.Message(time_queue[rid][0], messages['yourtime']%(time_queue[rid][1], rdisplay), 'groupchat'))
        else:
            conn.send(xmpp.protocol.Message(time_queue[rid][0], messages['time']%(time_queue[rid][1], iq_obj.getFrom().getResource(), rdisplay), 'groupchat'))

def timeerrorCB(conn, iq_obj):
    rid=iq_obj.getID()
    if time_queue.has_key(rid):
        conn.send(xmpp.protocol.Message(time_queue[rid][0], messages['time_error']%(time_queue[rid][1], iq_obj.getFrom().getResource()), 'groupchat'))
