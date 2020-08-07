*** Settings ***
# For lib testing: 
#Library     ../robotframework_pykafka/robotframework_pykafka.py

# Normal way to import when installed from pip:
Library     robotframework_pykafka

*** Test Cases ***
Test Producing and Consuming a Message
    [Documentation]  Tests text messaging in and out of a sample kafka streams
    ...              app at https://github.com/invadergir/kafka-streams-scala-template
    ...              To run, start kafka, get the above app running, and create
    ...              the topics mentioned below.

    ${inputTopic}=  Set Variable  input
    ${outputTopic}=  Set Variable  output

    # Reset the offset before producing anything so we don't consume anything 
    # we don't care about:
    Kafka Set Consumer Offset To Latest  ${outputTopic}

    # Send a message on the input topic:
    Kafka Produce  ${inputTopic}  A  AAA

    # Wait a bit
    sleep  1s  Wait for kafka and app to process the message

    # The service should produce two messages for each input message:
    ${output}=  Kafka Consume String  ${outputTopic}
    should be equal as strings  ${output[0]}  A
    should be equal as strings  ${output[1]}  AAA

    ${output}=  Kafka Consume String  ${outputTopic}
    should be equal as strings  ${output[0]}  A
    # second message just adds XXX on the end of value:
    should be equal as strings  ${output[1]}  AAAXXX

