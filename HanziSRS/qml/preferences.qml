import QtQuick.Window 2.2
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.3
import QtQml 2.2
import QtQuick 2.7

Window {
    id: root
    title: "Preferences"
    width: 600
    height: 600

    ColumnLayout {
        id: overall
        anchors.margins: 10
        anchors.fill: parent

        RowLayout {
            id: contents
            anchors.fill: parent
            spacing: 20

            Rectangle {
                width: 150
                height: 500

                border.color: "gray"

                ListView {
                    id: list
                    anchors.fill: parent
                    anchors.margins: 10

                    model: ListModel {
                        ListElement { name: "Credentials" }     // 0
                        ListElement { name: "User dictionary" } // 1
                        ListElement { name: " • Vocabulary" }   // 2
                        ListElement { name: " • Hanzi" }        // 3
                        ListElement { name: " • Reading" }      // 4
                        ListElement { name: "User database" }   // 5
                        ListElement { name: " • Vocabulary" }   // 6
                        ListElement { name: " • Hanzi" }        // 7
                        ListElement { name: " • Reading" }      // 8
                        ListElement { name: "Preferences" }     // 9
                    }
                    delegate: Item {
                        width: parent.width
                        height: 20

                        Text {
                            text: name
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                list.currentIndex = index

                                var all = {
                                    "0": credentials,
                                    "9": preferences
                                }
                                for(var i in all){
                                    all[i].visible = false
                                }
                                all[parseInt(index)].visible = true
                            }
                        }
                    }
                    highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
                }
            }

            ColumnLayout {
                id: credentials
                anchors.top: parent.top
                visible: true

                Rectangle { height: 30 }

                GridLayout {
                    columns: 2

                    Label { text: "User's full name : " }
                    TextField {
                        id: fullName
                        Layout.fillWidth: true
                    }
                }

                Rectangle { height: 30 }

                GridLayout {
                    columns: 2

                    Label { text: "HSK vocabulary level : " }
                    SpinBox {
                        id: vocabLevel
                        Layout.fillWidth: true
                        textFromValue: function(value, locale) {
                            return 'HSK level ' + value
                        }
                        valueFromText: function(text, locale) {
                            return parseInt(text.match(/HSK level \d+/))
                        }
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
            }

            ColumnLayout {
                id: preferences
                anchors.top: parent.top
                visible: false

                Rectangle { height: 30 }

                RowLayout {
                    CheckBox {
                        id: atLeastTwoChar
                        checked: false
                        text: "Learn only words that are least 2 characters long"
                        onClicked: {
                            console.log(checked)
                        }
                    }
                }
            }
        }

        RowLayout {
            id: buttons
            implicitHeight: 50
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Button {
                id: ok
                text: "OK"
                onClicked: {
                    var params = {
                        'vocab_level': vocabLevel.value,
                        'hanzi_level': hanziLevel.text,
                        'reading_level': readingLevel.text
                    }
                    pyUser.set_cred(JSON.stringify(params))
                    root.close()
                }
            }
        }
    }

    Component.onCompleted: {
        var user = JSON.parse(pyUser.get_user)
        var cred = user.cred
        atLeastTwoChar.checked = user.settings.at_least_2_char

        vocabLevel.value = cred.vocab_level
        hanziLevel.text = cred.hanzi_level
        readingLevel.text = cred.reading_level
    }
}