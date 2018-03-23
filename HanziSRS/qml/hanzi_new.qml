import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7

Window {
    width: 600
    height: 400
    x: 200
    y: 200
    id: root

    RowLayout {
        anchors.margins: 10
        anchors.fill: parent

        ColumnLayout {
            spacing: 20
            anchors.top: parent.top

            Label {
                property bool match: false
                property var previous: []
                property int charNumber: 0

                color: match ? "green" : "black"

                id: character
                font.pointSize: 200
                Layout.preferredWidth: 200
                Layout.preferredHeight: 200
            }

            RowLayout {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Button {
                    id: previousCharButton
                    text: "Previous"
                    enabled: false
                    onClicked: {
                        character.charNumber--
                        new_char(character.previous[character.charNumber])

                        if(character.charNumber <= 0)
                            previousCharButton.enabled = false
                    }
                }
                Button {
                    id: nextCharButton
                    text: "Next"
                    onClicked: {
                        character.charNumber++
                        var ch
                        if(character.charNumber < character.previous.length)
                            ch = character.previous[character.charNumber]
                        else {
                            ch = getRandChar()
                            character.previous.push(ch)
                        }
                        new_char(ch)

                        previousCharButton.enabled = true
                    }
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

    property string characterPool: ''

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

        pyHanziVariant.do_lookup(_char)
        var variants = JSON.parse(pyHanziVariant.get_lookup)
        var variant
        for(var m=0; m<variants.length; m++){
            variant = variants[m]['Character'] + variants[m]['Variant']
            for(var n=0; n<variant.length; n++){
                pySentence.do_lookup(variant[n])
                var sen = JSON.parse(pySentence.get_lookup)
                for(i=0; i<sen.length; i++){
                    rel_sen_text += "<a href='"+ sen[i].Chinese + "'>"
                                    + sen[i].Chinese + "</a> "
                                    + sen[i].English + "<br />"
                }
            }
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

    function getRandChar(){
        var index = Math.floor(Math.random() * root.characterPool.length);
        character.text = root.characterPool[index]

        return root.characterPool[index]
    }

    Component.onCompleted: {
        var all_chars = JSON.stringify(pyUserVocab.get_dump)
                    + JSON.stringify(pyUserSentence.get_dump)
        for(var i=0; i<all_chars.length; i++){
            if(all_chars[i] >= '\u4e00' && all_chars[i] <= '\u9fff'){
                if(root.characterPool.indexOf(all_chars[i]) === -1){
                    root.characterPool += all_chars[i]
                }
            }
        }

        new_char(getRandChar())
    }
}