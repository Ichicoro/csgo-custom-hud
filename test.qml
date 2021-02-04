import QtQuick 2.0
import QtQuick.Controls 2.15

Item {
  property var lineHeight: 24

  width: 224
  height: 122

  Column {
    anchors.fill: parent
    spacing: 2

    Row {
      id: ammo_row
      width: parent.width
      height: lineHeight

      ProgressBar {
        id: ammo_progressBar
        value: 0.5
        anchors.fill: parent
        smooth: true
        indeterminate: false

        background: Rectangle {
            anchors.fill: progressBar
            color: "#2e2f30"
        }

        contentItem: Rectangle {
          height: parent.height
          width: parent.width * parent.value
          anchors.left: parent.left
          anchors.bottom: parent.bottom
          color: "#FFA200"
        }
      }

      Label {
        id: magammo_label
        height: parent.height
        text: "50"
        width: parent.width / 2
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        font.bold: false
        leftPadding: 3
        font.pointSize: 16
        font.family: "Bahnschrift SemiBold"
      }

      Label {
        id: magsize_label
        height: parent.height
        text: "50"
        width: parent.width / 2
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        rightPadding: 3
        font.pointSize: 16
        font.family: "Bahnschrift SemiBold"
      }

      Label {
        id: weapon_name_label
        height: parent.height
        text: "AK-48"
        width: parent.width
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        rightPadding: 3
        font.pointSize: 14
        font.family: "Bahnschrift SemiBold"
      }
    }


    Row {
      id: health_row
      width: parent.width
      height: lineHeight

      ProgressBar {
        id: health_progressBar
        value: 0.5
        anchors.fill: parent
        smooth: true
        indeterminate: false

        background: Rectangle {
            anchors.fill: parent
            color: "#2e2f30"
        }

        contentItem: Rectangle {
          height: parent.height
          width: parent.width * parent.value
          anchors.left: parent.left
          anchors.bottom: parent.bottom
          color: "#BF3838"
        }
      }

      Label {
        id: currHP_label
        height: parent.height
        text: "50"
        width: parent.width / 2
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        font.bold: false
        leftPadding: 3
        font.pointSize: 16
        color: "white"
        font.family: "Bahnschrift SemiBold"
      }

      Label {
        height: parent.height
        text: "HP"
        width: parent.width / 2
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        font.capitalization: Font.Capitalize
        rightPadding: 3
        font.pointSize: 16
        color: "white"
        font.family: "Bahnschrift SemiBold"
      }
    }


    Row {
      id: armor_row
      width: parent.width
      height: lineHeight

      ProgressBar {
        id: armor_progressBar
        anchors.fill: parent
        value: 0.5
        smooth: true
        indeterminate: false

        background: Rectangle {
            anchors.fill: parent
            color: "#2e2f30"
        }

        contentItem: Rectangle {
          height: parent.height
          width: parent.width * parent.value
          anchors.left: parent.left
          anchors.bottom: parent.bottom
          color: "#3838bf"
        }
      }

      Label {
        id: currarmor_label
        height: parent.height
        text: "50"
        width: parent.width / 2
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        verticalAlignment: Text.AlignVCenter
        font.bold: false
        leftPadding: 3
        font.pointSize: 16
        color: "white"
        font.family: "Bahnschrift SemiBold"
      }

      Label {
        height: parent.height
        text: "ARMOR"
        width: parent.width / 2
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        horizontalAlignment: Text.AlignRight
        verticalAlignment: Text.AlignVCenter
        font.capitalization: Font.Capitalize
        rightPadding: 3
        font.pointSize: 16
        color: "white"
        font.family: "Bahnschrift SemiBold"
      }
    }
  }

}


