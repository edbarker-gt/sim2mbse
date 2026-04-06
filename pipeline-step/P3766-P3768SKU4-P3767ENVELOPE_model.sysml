package P3766_P3768SKU4_P3767ENVELOPE {

  part def Usb32TypeC {}
  part def Usb32TypeAStacked {}
  part def Rj45Ethernet {}
  part def DisplayPort {}
  part def M2KeyE {}
  part def M2KeyM4Lane {}
  part def M2KeyM2Lane {}
  part def CameraConnector {}
  part def ExpansionHeader40Pin {}
  part def ButtonHeader {}
  part def CanBusHeader {}
  part def FanConnector {}
  part def DcPowerJack {}
  part def OtherPort {}

  part BoardAssembly {

    part usb32TypeC : Usb32TypeC;
    part usb32TypeAStacked : Usb32TypeAStacked;
    part gigabitEthernet : Rj45Ethernet;
    part displayPort : DisplayPort;
    part m2KeyE : M2KeyE;
    part m2KeyM4Lane : M2KeyM4Lane;
    part m2KeyM2Lane : M2KeyM2Lane;
    part cameraConnector : CameraConnector;
    part expansionHeader40Pin : ExpansionHeader40Pin;
    part buttonHeader : ButtonHeader;
    part canBusHeader : CanBusHeader;
    part fanConnector : FanConnector;
    part dcPowerJack : DcPowerJack;

  }
}
