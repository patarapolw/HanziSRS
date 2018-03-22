import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7

Window {
    width: 600
    height: 400
    x: 200
    y: 200

    RowLayout {
        anchors.margins: 10
        anchors.fill: parent

        ColumnLayout {
            spacing: 20
            anchors.top: parent.top

            Label {
                property bool match: false
                color: match ? "green" : "black"

                id: character
                font.pointSize: 200
                Layout.preferredWidth: 200
                Layout.preferredHeight: 200
            }
            Label {
                text: "<a href='#'>Next character</a>"
                onLinkActivated: {
                    new_char(pyUserVocab.get_rand_char)
                }
            }
        }

        ColumnLayout {
            Label { text: "Related characters : "}
            TextField {
                property bool match: false
                background: Rectangle {
                    border.color: "gray"
                    color: rel_char.match ? "#badc58" : "#ffffff"
                }

                id: rel_char
                Layout.fillWidth: true
                onTextEdited: {
                    checkInDatabase()
                }
            }

            Label { text: "Related vocabularies : "}
            TextField {
                property bool match: false
                background: Rectangle {
                    border.color: "gray"
                    color: rel_vocab.match ? "#badc58" : "#ffffff"
                }

                id: rel_vocab
                Layout.fillWidth: true
                onTextEdited: {
                    checkInDatabase()
                }
                onAccepted: {
                    saveOrRemove.click()
                }
            }

            Label { text: "Related sentences : "}
            ScrollView {
                implicitHeight: 200
                Layout.fillWidth: true

                TextArea {
                    id: rel_sen
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

            RowLayout {
                anchors.right: parent.right

                Button {
                    property bool save: true

                    id: saveOrRemove
                    text: save ? "Save" : "Remove"
                    onClicked: {
                        if(saveOrRemove.save) {
                            pyUserHanzi.do_submit(character.text, rel_char.text, rel_vocab.text)
                            character.match = true
                            rel_char.match = true
                            rel_char.match = true
                            rel_vocab.match = true

                            saveOrRemove.save = false
                        } else {
                            pyUserHanzi.do_delete(character.text)
                            character.match = false
                            rel_char.match = false
                            rel_vocab.match = false

                            saveOrRemove.save = true
                        }
                    }
                }
                Button {
                    id: reset
                    text: "Reset"
                    enabled: false
                    onClicked: {
                        new_char(character.text)
                    }
                }
            }
        }
    }

    function new_char(_char) {
        character.text = _char

        var rel_vocab_text = []
        var database = pyUserVocab.get_dump
        for(var i=0; i<database.length; i++){
            if(database[i].join().indexOf(character.text) != -1)
                rel_vocab_text.push(database[i][1])
        }
        rel_vocab.text = rel_vocab_text.join('，')

        var rel_sen_text = ''
        pySentence.do_lookup(_char)
        var sen = JSON.parse(pySentence.get_lookup)
        for(i=0; i<sen.length; i++){
            rel_sen_text += "<a href='"+ sen[i].Chinese + "'>"
                            + sen[i].Chinese + "</a> "
                            + sen[i].English + "<br />"
        }
        rel_sen.text = rel_sen_text

        pyUserHanzi.do_lookup(_char)
        var lookup = pyUserHanzi.get_lookup
        if(lookup.length === 2){
            rel_char.text = lookup[0]
            rel_vocab.text = lookup[1]
        } else {
            rel_char.text = ""
        }

        checkInDatabase()
    }

    function checkInDatabase() {
        var lookup = pyUserHanzi.get_lookup
        if(lookup.length !== 0){
            character.match = true
            saveOrRemove.save = true

            if(lookup[0] == rel_char.text){
                rel_char.match = true
            } else {
                rel_char.match = false
            }
            if(lookup[1] == rel_vocab.text){
                rel_vocab.match = true
            } else {
                rel_vocab.match = false
            }
        } else {
            character.match = false
            saveOrRemove.save = false

            rel_char.match = false
            rel_vocab.match = false
        }

        if(rel_char.text){
            saveOrRemove.save = true
            reset.enabled = true
        } else {
            saveOrRemove.save = false
            reset.enabled = false
        }

        return lookup
    }

    Component.onCompleted: {
        new_char(pyUserVocab.get_rand_char)
    }
}