import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7
import QtQml 2.2

Window {
    id: root
    title: "Explore new sentences"
    width: 800
    height: 400
    visible: true

    ColumnLayout {
        anchors.margins: 10
        anchors.fill: parent

        RowLayout {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.topMargin: 20
            anchors.rightMargin: 20

            ColumnLayout {
                RowLayout {
                    Text {
                        text: "-"
                        MouseArea {
                            id: minusSlider

                            anchors.fill: parent
                            onClicked: {
                                level.decrease()
                                loadSentence(level.value)
                            }
                        }
                    }
                    Slider {
                        id: level
                        stepSize: 1
                        onMoved: {
                            loadSentence(value)
                        }
                    }
                    Text {
                        text: "+"
                        MouseArea {
                            id: plusSlider

                            anchors.fill: parent
                            onClicked: {
                                level.increase()
                                loadSentence(level.value)
                            }
                        }
                    }
                }

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: level.value + " of " + root.sentences.length + " sentences"
                }
            }


        }

        ColumnLayout {
            spacing: 20
            anchors.horizontalCenter: parent.horizontalCenter

            Label {
                property bool match: false

                id: sentence
                anchors.horizontalCenter: parent.horizontalCenter
                text: "普通话汉字"
                font.pointSize: 50
                color: match ? "green" : "black"

                focus: true
                Keys.onLeftPressed: minusSlider.clicked(Qt.LeftButton)
                Keys.onRightPressed: plusSlider.clicked(Qt.LeftButton)
                Keys.onReturnPressed: speak.clicked(Qt.LeftButton)
                Keys.onSpacePressed: saveOrRemove.clicked(Qt.LeftButton)
            }
            Label {
                id: english
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Welcome to Thailand!"
                color: sentence.match ? "green" : "black"
            }
        }

        Button {
            anchors.horizontalCenter: parent.horizontalCenter

            id: speak
            text: "Speak"
            onClicked: {
                py.speak(sentence.text)
            }
        }

        RowLayout {
            spacing: 30

            ColumnLayout {
                width: 350
                anchors.top: parent.top

                Label { text: "Related vocabularies : "  }
                TextField {
                    property bool match: false

                    background: Rectangle {
                        border.color: "gray"
                        color: rel_vocab.match ? "#badc58" : "white"
                    }

                    id: rel_vocab
                    implicitWidth: parent.width
                    onTextEdited: {
                        checkInUserDatabase()
                    }
                }

                Label { text: "Related Hanzi : " }
                TextField {
                    property bool match: false

                    background: Rectangle {
                        border.color: "gray"
                        color: rel_hanzi.match ? "#badc58" : "white"
                    }

                    id: rel_hanzi
                    implicitWidth: parent.width
                    onTextEdited: {
                        checkInUserDatabase()
                    }
                }
            }

            ColumnLayout {
                Label { text: "Notes : " }
                ScrollView {
                    implicitHeight: 100
                    Layout.fillWidth: true
                    background: Rectangle {
                        border.color: "gray"
                        color: notes.match ? "#badc58" : "white"
                    }

                    TextArea {
                        property bool match: false

                        id: notes
                        height: parent.height
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }

        RowLayout {
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Button {
                id: saveOrRemove
                text: sentence.match ? "Remove" : "Save"
                onClicked: {
                    if(sentence.match){
                        pyUserSentence.do_delete(sentence.text)
                        sentence.match = false
                    } else {
                        saveToUserSentence(0)
                        sentence.match = true
                    }
                }
            }
            Button {
                id: addToLearning
                text: "Add to learning"
                onClicked: {
                    saveToUserSentence(1)
                    addToLearning.enabled = false
                }
            }
            Button {
                id: addToReview
                text: "Add to review"
                onClicked: {
                    saveToUserSentence(2)
                    addToReview.enabled = false
                }
            }
        }
    }

    property var sentences: []
    property var user

    Component.onCompleted: {
        var sentences = JSON.parse(pySentence.get_dump)
        for(var key in sentences){
            root.sentences.push(sentences[key])
        }
        level.from = 1
        level.to = root.sentences.length

        root.user = JSON.parse(pyUser.get_user)
        level.value = root.user.state.sentence

        loadSentence(level.value)
    }

    onClosing: {
        root.user.state.sentence = level.value
        pyUser.set_user(JSON.stringify(root.user))
    }

    function loadSentence(value){
        var index = Math.floor(value-1)
        sentence.text = root.sentences[index].Chinese
        english.text = root.sentences[index].English

        checkInUserDatabase()
    }

    function saveToUserSentence(type){
        pyUserSentence.do_submit([sentence.text, rel_hanzi.text, rel_vocab.text,
                                    notes.text, type, 0, 0])
        sentence.match = true
    }

    function checkInUserDatabase(){
        pyUserSentence.do_lookup(sentence.text)
        if(pyUserSentence.get_lookup.length === 0){
            sentence.match = false
        } else {
            sentence.match = true
        }
    }
}
