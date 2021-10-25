# postalservice
I didn't like how difficult it was to make my programs communicate. Because of that I applied a bit of lazy juice, and now it's easy. for me. ;)

postservice.py opens a server on port 28729, as of 25. Oct 2021.

each message the server receives should start with "<<START>>" and end with "<<END>>". Please note that all messages should be ASCII
  if the first seven digits of the received message (not counting <<START>>) are "SETRECV" then
    the server will make the remaining characters in the message in a dictionary, to which the value is a list containing the client.
 
  otherwise the server will split the message into two string, splitting by "<<||>>". it will then send a copy of the originally received message to all client registered to the key.

  

postcomm.py is the client side module for dealing with the server.
  it contains the class PostController. Which when initialized takes two OPTIONAL values. host and port. The default values match the default values of the server.
  
  .tag(self, tag)
    takes a string value and adds it as a 'tag', this means any message written to the tag will be sent to the client.
  
  .tags(self, tags)
    same as the above, but takes a list of tags instead of a single string.
  
  .readable(self)
    returns True if a message can be read. if not returns false.
    NOTE: I am fairly certain, that my understanding of sockets and checking for available messages is wrong.
  
  .read(self)
    if a message has been received from server. returns said message and the tag the message was sent with. i.e. return message, tag
    if a message has not yet been received it will block until a message is received, then it will return it.
  
  .send(mess, tag)
    sends a message to a tag.
