import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQml 2.2

Window {
    id: root
    width: 300
    height: 200

    ColumnLayout {
        anchors.margins: 10
        anchors.fill: parent

        GridLayout {
            columns: 2

            Label { text: "HSK vocabulary level : " }
            TextField {
                id: vocabLevel
                Layout.fillWidth: true
            }

            Label { text: "Hanzi Level Project Hanzi level : " }
            TextField {
                id: hanziLevel
                Layout.fillWidth: true
            }

            Label { text: "SpoonFed Reading level : " }
            TextField {
                id: readingLevel
                Layout.fillWidth: true
            }
        }

        RowLayout {
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Button {
                id: ok
                text: "OK"
                onClicked: {
                    pyUserCred.set_vocab_level(vocabLevel.text)
                    pyUserCred.set_hanzi_level(hanziLevel.text)
                    pyUserCred.set_reading_level(readingLevel.text)
                    root.close()
                }
            }
        }
    }

    Component.onCompleted: {
        vocabLevel.text = pyUserCred.get_vocab_level
        hanziLevel.text = pyUserCred.get_hanzi_level
        readingLevel.text = pyUserCred.get_reading_level
    }
}