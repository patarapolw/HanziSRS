import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7
import QtQml 2.2


Window {
    visible: true
    id: root
    width: 400
    height: 200

    signal activated(var tags)

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
                    var tags = tagInput.text.trim().split(" ")
                    if(tags.every(inCategory)){
                        root.activated(tags)
                        root.close()
                    } else {
                        console.log("Not match")
                    }

                    function inCategory(tag){
                        return root.categoryCount.map(function(x){return x[0]}).indexOf(tag) !== -1
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
                    tagInput.text += (" " + link + " ")
                }
            }
        }
    }

    property var categoryCount

    Component.onCompleted: {
        var raw = JSON.parse(pyVocabCategory.get_categories)
        var sortable = []
        for(var key in raw) sortable.push([key, raw[key]])
        root.categoryCount = sortable.sort(function(a, b){return b[1] - a[1]})

        parseTags()
    }

    function parseTags(){
        if(!tagInput.text){
            tagNames.text = "Or choose from below : "
            for(var i=0; i<root.categoryCount.length; i++){
                tagNames.text += "<a href='" + root.categoryCount[i][0] + "'>"
                    + root.categoryCount[i][0] + " ("
                    + root.categoryCount[i][1] + ")</a> "
            }
        } else {
            tagNames.text = ""
            for(var i=0; i<root.categoryCount.length; i++){
                if(root.categoryCount[i][0].indexOf(tagInput.text) !== -1){
                    tagNames.text += "<a href='" + root.categoryCount[i][0] + "'>"
                        + root.categoryCount[i][0] + " ("
                        + root.categoryCount[i][1] + ")</a> "
                }
            }
        }
    }
}