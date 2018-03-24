import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQuick 2.7

Window {
    visible: true
    id: root
    height: 500
    width: 1000

    ScrollView {
        anchors.fill: parent

        TextArea {
            id: hanziList
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

    Component.onCompleted: {
        var levels = JSON.parse(pyHanziLevel.get_levels)
        var all_chars = pyUserVocab.get_dump
                    + pyUserSentence.get_dump
        var characterPool = ''
        for(var i=0; i<all_chars.length; i++){
            if(all_chars[i] >= '\u4e00' && all_chars[i] <= '\u9fff'){
                if(characterPool.indexOf(all_chars[i]) === -1){
                    characterPool += all_chars[i]
                }
            }
        }

        var oneLevel
        var previousLabel = ''
        for(var i=0; i<levels.length; i++){
            if(levels[i][1] !== previousLabel){
                hanziList.text += "<h2>" + levels[i][1] + "</h2>"
                previousLabel = levels[i][1]
            }

            oneLevel = "Level " + ("   " +(i+1)).slice(-3) + " : "
            for(var j=0; j<levels[i][0].length; j++){
                if(characterPool.indexOf(levels[i][0][j]) !== -1){
                    oneLevel += "<font color='gray'>" + levels[i][0][j] + "</font>"
                } else {
                    oneLevel += "<font color='white'>" + levels[i][0][j] + "</font>"
                }
            }
            hanziList.text += oneLevel
        }
    }
}