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

    port usb32TypeC: Usb32TypeC;
    port usb32TypeAStacked: Usb32TypeAStacked;
    port gigabitEthernet: Rj45Ethernet;
    port displayPort: DisplayPort;
    port m2KeyE: M2KeyE;
    port m2KeyM4Lane: M2KeyM4Lane;
    port m2KeyM2Lane: M2KeyM2Lane;
    port cameraConnector: CameraConnector;
    port expansionHeader40Pin: ExpansionHeader40Pin;
    port buttonHeader: ButtonHeader;
    port canBusHeader: CanBusHeader;
    port fanConnector: FanConnector;
    port dcPowerJack: DcPowerJack;

  }
}
