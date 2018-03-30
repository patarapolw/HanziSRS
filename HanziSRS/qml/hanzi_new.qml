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
    visible: true

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

            RowLayout {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Button {
                    id: previousCharButton
                    text: "Previous"
                    enabled: false
                    onClicked: {
                        root.currentCharIndex--
                        new_char(root.characterPool[root.currentCharIndex])

                        nextCharButton.enabled = true
                        if(root.currentCharIndex <= 0)
                            previousCharButton.enabled = false
                    }
                }
                Button {
                    id: nextCharButton
                    text: "Next"
                    onClicked: {
                        root.currentCharIndex++
                        new_char(root.characterPool[root.currentCharIndex])

                        previousCharButton.enabled = true
                        if(root.currentCharIndex >= root.characterPool.length-1)
                            nextCharButton.enabled = false
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
                    color: rel_hanzi.match ? "#badc58" : "#ffffff"
                }

                id: rel_hanzi
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
            }

            Label { text: "Related sentences : "}
            ScrollView {
                implicitHeight: 100
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

            Label { text: "Notes : "}
            ScrollView {
                implicitHeight: 100
                Layout.fillWidth: true
                background: Rectangle {
                    anchors.fill: parent
                    border.color: "gray"
                }

                TextArea {
                    id: notes
                    height: parent.height
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    readOnly: false
                }
            }

            RowLayout {
                anchors.right: parent.right
                anchors.bottom: parent.bottom

                Button {
                    id: saveOrRemove
                    text: character.match ? "Remove" : "Save"
                    onClicked: {
                        if(character.match){
                            pyUserHanzi.do_delete(character.text)
                            character.match = false
                        } else {
                            saveToUserHanzi(0)
                            character.match = true
                        }
                    }
                }
                Button {
                    id: addToLearning
                    text: "Add to learning"
                    onClicked: {
                        saveToUserHanzi(1)
                        addToLearning.enabled = false
                    }
                }
                Button {
                    id: addToReview
                    text: "Add to review"
                    onClicked: {
                        saveToUserHanzi(2)
                        addToReview.enabled = false
                    }
                }
            }
        }
    }

    property var characterPool: []
    property int currentCharIndex: 0

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
            rel_hanzi.text = lookup[0]
            rel_vocab.text = lookup[1]
        } else {
            rel_hanzi.text = ""
        }

        checkInDatabase()
    }

    function checkInDatabase() {
        var lookup = pyUserHanzi.get_lookup
        if(lookup.length !== 0){
            character.match = true

            if(lookup[0] == rel_hanzi.text){
                rel_hanzi.match = true
            } else {
                rel_hanzi.match = false
            }
            if(lookup[1] == rel_vocab.text){
                rel_vocab.match = true
            } else {
                rel_vocab.match = false
            }
        } else {
            character.match = false

            rel_hanzi.match = false
            rel_vocab.match = false
        }

        return lookup
    }

    function shuffleArray(array) {
        for (var i = array.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }

    function saveToUserHanzi(type){
        pyUserHanzi.do_submit([character.text, rel_hanzi.text, rel_vocab.text,
                                    notes.text, type.text, 0, 0])
        character.match = true
    }

    Component.onCompleted: {
        var all_chars = JSON.stringify(pyUserVocab.get_dump)
                    + JSON.stringify(pyUserSentence.get_dump)
        for(var i=0; i<all_chars.length; i++){
            if(all_chars[i] >= '\u4e00' && all_chars[i] <= '\u9fff'){
                if(root.characterPool.indexOf(all_chars[i]) === -1){
                    root.characterPool.push(all_chars[i])
                }
            }
        }

        shuffleArray(root.characterPool)
        new_char(root.characterPool[root.currentCharIndex])

        if(root.characterPool.length === 1)
            nextCharButton.enabled = false
    }
}