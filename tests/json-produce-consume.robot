*** Settings ***
# For lib testing: 
#Library     ../robotframework_pykafka/robotframework_pykafka.py

# Normal way to import when installed from pip:
Library     robotframework_pykafka

# Needed for JSON manipulation:
Library     JSONLibrary

*** Test Cases ***
Test Producing and Consuming a Message
    [Documentation]  Tests JSON messaging in and out of a sample kafka streams 
    ...              app at https://github.com/invadergir/kafka-streams-scala-template
    ...              To run, start kafka, get the above app running, and create 
    ...              the topics mentioned below. 

    ${inputTopic}=  Set Variable  input
    ${outputTopic}=  Set Variable  output

    # Reset the offset before producing anything so we don't consume anything 
    # we don't care about:
    Kafka Set Consumer Offset To Latest  ${outputTopic}

    # Send a message on the input topic:
    ${inputJson}=  catenate
    ...  {
    ...    "A":"AAA",
    ...    "B":"BBB"
    ...  }
    Kafka Produce  ${inputTopic}  A   ${inputJson}

    # Wait a bit
    sleep  1s  Wait for kafka and app to process the message

    # The service should produce two messages for each input message:

    # Compare the strings - this is BAD because you can't rely on the order 
    # of the fields being the same:
    #${output}=  Kafka Consume String  ${outputTopic}
    #should be equal as strings  ${output[0]}       A
    #should be equal as strings  ${output[1]}     {"A":"AAA","B":"BBB"}

    # Instead, compare the values as dicts
    ${outputJson}=  Kafka Consume Json  ${outputTopic}
    should be equal as strings   ${outputJson[0]}    A
    ${expectedValue}=  Create Dictionary  
    ...  A=AAA  
    ...  B=BBB
    should be equal              ${outputJson[1]}    ${expectedValue}
    
    # second message just adds X on the end of value:
    ${outputJson}=  Kafka Consume Json  ${outputTopic}
    should be equal as strings   ${outputJson[0]}    A
    ${expectedValue}=  Create Dictionary  
    ...  A=AAA  
    ...  B=BBB  
    ...  X=XXX
    should be equal              ${outputJson[1]}    ${expectedValue}

    # Note that if you change the order of the entries in the dict, it won't matter.
    # You must compare json by comparing the dict forms, in case ordering changes:
    ${expectedValue}=  Create Dictionary  X=XXX  B=BBB  A=AAA
    should be equal              ${outputJson[1]}    ${expectedValue}

    # Only two messages should have been output (nothing will be in the topic)
    ${outputJson}=  Kafka Consume Json  ${outputTopic}
    should be equal  ${None}  ${outputJson}

