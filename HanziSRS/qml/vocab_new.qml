import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7
import QtQml 2.2

Window {
    id: root
    width: 800
    height: 400

    ColumnLayout {
        anchors.margins: 10
        anchors.fill: parent

        RowLayout {
            ColumnLayout {
                width: 300
                spacing: 30

                Label {
                    property int currentVocabIndex

                    id: vocabSimp
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "普通话汉字"
                    font.pointSize: 50
                }

                RowLayout {
                    spacing: 30

                    anchors.horizontalCenter: parent.horizontalCenter
                    Button {
                        id: previousVocab
                        text: "Previous"
                        enabled: false
                        onClicked: {
                            vocabSimp.currentVocabIndex--
                            setDictionaryEntry(vocabSimp.currentVocabIndex, 0)

                            nextVocab.enabled = true
                            if(vocabSimp.currentVocabIndex-1 < 0){
                                previousVocab.enabled = false
                            }
                        }
                    }
                    Button {
                        id: nextVocab
                        text: "Next"
                        enabled: true
                        onClicked: {
                            vocabSimp.currentVocabIndex++
                            setDictionaryEntry(vocabSimp.currentVocabIndex, 0)

                            previousVocab.enabled = true
                            if(vocabSimp.currentVocabIndex+1 >= root.vocabList.length){
                                nextVocab.enabled = false
                            }
                        }
                    }
                }
            }

            ColumnLayout {
                RowLayout {
                    Rectangle {
                        width: 100

                        Label {
                            id: vocabTrad
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "普通話漢字"
                            font.pointSize: 30
                        }
                    }

                    ColumnLayout {
                        RowLayout {
                            Label { text: "Reading : "}
                            Label {
                                id: pinyin
                                textFormat: TextEdit.RichText
                                onLinkActivated: {
                                    py.speak(link)
                                }
                            }
                        }

                        RowLayout {
                            Label { text: "Meanings : "}
                            ScrollView {
                                implicitHeight: 50
                                Layout.fillWidth: true

                                TextArea {
                                    id: english

                                    height: parent.height
                                    Layout.fillWidth: true
                                    wrapMode: Text.WordWrap
                                    textFormat: TextEdit.RichText
                                    readOnly: true
                                    onLinkActivated: {
                                        setDictionaryEntry(vocabSimp.currentVocabIndex, link)

                                        var line_previous_next_meaning = ''
                                        if(link-1 >= 0){
                                            line_previous_next_meaning +=
                                                "<a href='" + (link-1) + "'>Previous Meaning</a>"
                                        }
                                        if(link < root.vocabList[vocabSimp.currentVocabIndex].length-1){
                                            line_previous_next_meaning +=
                                                "<a href='" + (link+1) + "'>Next Meaning</a>"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }

                ColumnLayout {
                    Label {
                        text: "Sentences : "
                        anchors.topMargin: 20
                        anchors.bottom: sentenceArea.top
                    }
                    ScrollView {
                        id: sentenceArea
                        implicitHeight: 100
                        Layout.fillWidth: true

                        TextArea {
                            id: sentences
                            height: parent.height
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            textFormat: TextEdit.RichText
                            readOnly: true
                            onLinkActivated: {
                                py.speak(link)
                            }
                        }
                    }
                }
            }
        }

        RowLayout {
            spacing: 30

            ColumnLayout {
                width: 350
                anchors.top: parent.top

                Label { text: "Associated sounds : "  }
                TextField {
                    property bool match: false
                    background: Rectangle {
                        border.color: "gray"
                        color: ass_sounds.match ? "#badc58" : "white"
                    }

                    id: ass_sounds
                    implicitWidth: parent.width
                    onTextEdited: {
                        checkInDatabase()
                    }
                }

                Label { text: "Associated meanings : " }
                TextField {
                    property bool match: false
                    background: Rectangle {
                        border.color: "gray"
                        color: ass_meanings.match ? "#badc58" : "white"
                    }

                    id: ass_meanings
                    implicitWidth: parent.width
                    onTextEdited: {
                        checkInDatabase()
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
                        color: "white"
                    }

                    TextArea {
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
                text: "Save"
                onClicked: {
                }
            }
            Button {
                id: addToLearning
                text: "Add to learning"
                onClicked: {
                }
            }
            Button {
                id: addToReview
                text: "Add to review"
                onClicked: {
                }
            }
        }
    }

    property var vocabList

    Component.onCompleted: {
        var level = pyUserCred.get_vocab_level
        var params = {
            "Old tag": "HSK_Level_" + level,
            "settings": {
                "at_least_2_char": true
            }
        }
        pyHskVocab.do_lookup_params(JSON.stringify(params))
        root.vocabList = JSON.parse(pyHskVocab.get_lookup_params)
        setDictionaryEntry(0, 0)
    }

    function setDictionaryEntry(index, entryNumber){
        var result = root.vocabList[index][entryNumber]

        vocabSimp.text = result["Simplified"]
        vocabTrad.text = result["Traditional"]
        pinyin.text = "<a href='" + result["Simplified"] + "'>"
            + result["HTML pinyin"] + "</a>"
        english.text = result["HTML meaning"]

        if(root.vocabList[index].length > 1){
            english.text += "<a href='" + 1 + "'>Next Meaning</a>"
        }

        pySentence.do_lookup(vocabSimp.text)
        var sen = JSON.parse(pySentence.get_lookup)
        sentences.text = ''

        for(var i=0; i<sen.length; i++){
            sentences.text += "<a href='" + sen[i]["Chinese"] + "'>"
                + sen[i]["Chinese"] + "</a> "
                + sen[i]["English"]
        }
    }
}