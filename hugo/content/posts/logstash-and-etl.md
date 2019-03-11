---
title: "Logstash and ETL"
date: 2019-03-07T01:14:10+08:00
draft: true
---

This is a post on how I try to relate ETL process when working with Logstash. In data-warehouse terminology, ETL (extract, transform, load) is a process where we extract data from its source, do any necessary transformation to that data, and load it to data repository. Logstash, on the other hand, is an open-source tool that can do such process.

<!--more-->

### Scenario

Let's assume that we are maintaining a messaging service that on top of storing messages in database, it also writes timestamp of message, message id, and message body to a log file. We want to have ability to query message body but we are not allowed to access the database. We have access to the log file, but the message body that's written there is hex-encoded. Here's a sample of the log file:

```
2019-03-07T01:54:01+0800 1239823 54686520717569636b2062726f776e20f09fa68a206a756d7073206f766572203133206c617a7920f09f90b62e
2019-03-07T01:55:01+0800 4339822 6e6f7720796f7520736565206d6521
2019-03-07T01:57:11+0800 4339825 6920776173206865782d656e636f646564207573696e67206f6e6c696e6520746f6f6c2061742068747470733a2f2f637279707469692e636f6d2f70697065732f6865782d6465636f646572
2019-03-07T02:04:01+0800 4332825 49207573656420746f207468696e6b20492077617320696e64656369736976652e20427574206e6f772049276d206e6f7420746f6f20737572652e
2019-03-07T02:05:10+0800 4314225 4c6966652069732073686f72742e20536d696c65207768696c6520796f75207374696c6c206861766520746565746821
2019-03-07T02:08:00+0800 4314320 416c776179732072656d656d626572207468617420796f7527726520756e697175652e202a4a757374206c696b652065766572796f6e6520656c73652a2e
```

#### Note

Above log file is space-separated value where the first column is message timestamp, followed by message id, and then the hex-encoded message body. To see the plaintext version of the first message body, we need to convert the message body from hex to ascii. Here's one way to do it (in ruby):

![decode hex to ascii using ruby](/images/irb-decode-hex.png)

> Once decoded, we know that `5468652071..` is `The quick brown..`.


### The Plan

We won't be able to query the messages without transforming the message body from hex to plain text. So, we come up with a plan:

1. Send the log file from its original location (ie. a vps where the service is running) to a *transformation layer*
2. Tell the *transformation layer* to convert each hex-encoded message body to plain text 
3. Push the transformed log to our data repository
4. Query the messages from data repository

what we have: 
log file of space-separated data. first column is the timestamp, followed by message id, and then message body (hex encoded).

what we want:

- timestamp
- message id
- message raw (hex)
- message decoded

plan:
- parse each line in logfile to *extract* timestamp, message id, and body to its respective fields. related: `input`
- *transform* the hex-encoded body to plaintext and store it to new field (body_plain). related: `filter`
- *load* the transformed log to output (file, elasticsearch, stdout, etc.). related: `output`

create filter. test in https://grokdebug.herokuapp.com
```
%{TIMESTAMP_ISO8601:timestamp} %{WORD:message_id} %{WORD:body_hex}
```

logstash filter


```
input {
  file {
    path => /var/log/messaging-service/messages.log
  }
}

filter {
  grok {
    match => "%{TIMESTAMP_ISO8601:timestamp} %{WORD:message_id} %{WORD:body_hex}"
  }

  mutate {
    add_field => ["decode_error"]
  }

  ruby {
    # attempt hex decode if payload doesn't contain
    # whitespace and its length is even number.
    code => "
      body_hex = event.get('[body_hex]')
      maybeHex = ...

      begin
        if maybeHex
          event.set('[body_plain]', [body_hex].pack('H*'))
        end
      rescue Exception => e
        event.set('[decode_error]', e.to_s())
      end
    "
  }
}

output {
  file {
    path => /opt/messaging-service/messages-plain.log
  }
}
```
