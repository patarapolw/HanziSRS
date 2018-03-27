import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7
import QtQml 2.2

Item {
    Window {
        visible: true
        id: dialog
        width: 400
        height: 200

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20

            Label {
                text: "Please enter a tag name : "
            }

            RowLayout {
                Layout.fillWidth: true

                TextField {
                    id: tagInput
                    Layout.fillWidth: true
                    onTextEdited: {
                        parseTags()
                    }
                    onAccepted: {
                        submit.clicked()
                    }
                }
                Button {
                    id: submit
                    text: "Submit"
                    onClicked: {
                        if(dialog.categoryCount.map(function(x){return x[0]}).indexOf(tagInput.text) !== -1){
                            main.setCategoryAndStart(tagInput.text)
                        } else {
                            console.log("Not match")
                        }
                    }
                }
            }

            ScrollView {
                implicitHeight: 100
                Layout.fillWidth: true

                TextArea {
                    id: tagNames
                    height: parent.height
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    textFormat: Text.RichText
                    readOnly: true
                    onLinkActivated: {
                        main.setCategoryAndStart(link)
                    }
                }
            }
        }

        property var categoryCount

        Component.onCompleted: {
            var raw = JSON.parse(pyVocabCategory.get_categories)
            var sortable = []
            for(var key in raw) sortable.push([key, raw[key]])
            dialog.categoryCount = sortable.sort(function(a, b){return b[1] - a[1]})

            parseTags()
        }

        function parseTags(){
            if(!tagInput.text){
                tagNames.text = "Or choose from below : "
                for(var i=0; i<dialog.categoryCount.length; i++){
                    tagNames.text += "<a href='" + dialog.categoryCount[i][0] + "'>"
                        + dialog.categoryCount[i][0] + " ("
                        + dialog.categoryCount[i][1] + ")</a> "
                }
            } else {
                tagNames.text = ""
                for(var i=0; i<dialog.categoryCount.length; i++){
                    if(dialog.categoryCount[i][0].indexOf(tagInput.text) !== -1){
                        tagNames.text += "<a href='" + dialog.categoryCount[i][0] + "'>"
                            + dialog.categoryCount[i][0] + " ("
                            + dialog.categoryCount[i][1] + ")</a> "
                    }
                }
            }
        }
    }

    Window {
        id: main
        title: "Learn new vocab"
        width: 800
        height: 400
        visible: false

        ColumnLayout {
            anchors.margins: 10
            anchors.fill: parent

            RowLayout {
                ColumnLayout {
                    width: 300
                    spacing: 30

                    Label {
                        property int currentVocabIndex
                        property bool match

                        id: vocabSimp
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "普通话汉字"
                        font.pointSize: 50
                        color: match ? "green" : "black"
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
                                main.setDictionaryEntry(vocabSimp.currentVocabIndex, 0)

                                nextVocab.enabled = true
                                if(vocabSimp.currentVocabIndex-1 < 0){
                                    previousVocab.enabled = false
                                }

                                main.checkInUserDatabase()
                                py.speak(vocabSimp.text)
                            }
                        }
                        Button {
                            id: nextVocab
                            text: "Next"
                            enabled: true
                            onClicked: {
                                vocabSimp.currentVocabIndex++
                                main.setDictionaryEntry(vocabSimp.currentVocabIndex, 0)

                                previousVocab.enabled = true
                                if(vocabSimp.currentVocabIndex+1 >= main.vocabList.length){
                                    nextVocab.enabled = false
                                }

                                main.checkInUserDatabase()
                                py.speak(vocabSimp.text)
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
                                            main.setDictionaryEntry(vocabSimp.currentVocabIndex, link)
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
                            main.checkInUserDatabase()
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
                            main.checkInUserDatabase()
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
                    text: vocabSimp.match ? "Remove" : "Save"
                    onClicked: {
                        if(vocabSimp.match){
                            pyUserVocab.do_delete(vocabSimp.text)
                            vocabSimp.match = false
                        } else {
                            main.saveToUserVocab(0)
                            vocabSimp.match = true
                        }
                    }
                }
                Button {
                    id: addToLearning
                    text: "Add to learning"
                    onClicked: {
                        main.saveToUserVocab(1)
                        addToLearning.enabled = false
                    }
                }
                Button {
                    id: addToReview
                    text: "Add to review"
                    onClicked: {
                        main.saveToUserVocab(2)
                        addToReview.enabled = false
                    }
                }
            }
        }

        property var vocabList

        function setCategoryAndStart(category) {
            dialog.close()
            main.visible = true

            var settings = JSON.parse(pyUser.get_user).settings

            pyVocabCategory.do_lookup_category(category)
            main.vocabList = JSON.parse(pyVocabCategory.get_lookup_category)
            main.setDictionaryEntry(0, 0)

            py.speak(vocabSimp.text)
        }

        function setDictionaryEntry(index, link){
            var result = main.vocabList[index]
            pyCedict.do_lookup(result['vocab'])
            var lookup = JSON.parse(pyCedict.get_lookup)

            vocabSimp.text = result["vocab"]
            pinyin.text = "<a href='" + result["vocab"] + "'>"
                + result["reading"] + "</a>"

            if(lookup.length !== 0){
                vocabTrad.text = lookup[link].traditional

                english.text = lookup[link].english

                english.text += "<br />Meaning " + (parseInt(link)+1) + " of "
                            + lookup.length + " "

                var line_next_meaning = ''
                if(link > 0){
                    line_next_meaning += "<a href='" + (parseInt(link)-1) + "'>Previous meaning</a> "
                }

                if(link < lookup.length-1){
                    line_next_meaning += "<a href='" + (parseInt(link)+1) + "'>Next meaning</a>"
                }
                english.text += line_next_meaning
            } else {
                vocabTrad.text = ''
                english.text = result["english"]
            }

            pySentence.do_lookup(vocabSimp.text)
            var sen = JSON.parse(pySentence.get_lookup)
            sentences.text = ''

            for(var i=0; i<sen.length; i++){
                sentences.text += "<a href='" + sen[i]["Chinese"] + "'>"
                    + sen[i]["Chinese"] + "</a> "
                    + sen[i]["English"]
            }

            main.checkInUserDatabase()
        }

        function saveToUserVocab(type){
            pyUserVocab.do_submit([vocabSimp.text, vocabTrad.text,
                                   ass_sounds.text, ass_meanings.text, notes.text, type, 0, 0])
            vocabSimp.match = true
        }

        function checkInUserDatabase(){
            pyUserVocab.do_lookup(vocabSimp.text)
            var result = pyUserVocab.get_lookup
            if(result.length !== 0){
                vocabSimp.match = true
            } else {
                vocabSimp.match = false
            }

            return result
        }
    }
}