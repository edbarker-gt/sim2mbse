package P3766_P3768SKU4_P3767ENVELOPE {

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

  interface Usb32TypeC { }
  interface Usb32TypeAStacked { }
  interface Rj45Ethernet { }
  interface DisplayPort { }
  interface M2KeyE { }
  interface M2KeyM4Lane { }
  interface M2KeyM2Lane { }
  interface CameraConnector { }
  interface ExpansionHeader40Pin { }
  interface ButtonHeader { }
  interface CanBusHeader { }
  interface FanConnector { }
  interface DcPowerJack { }
  interface OtherPort { }
}
