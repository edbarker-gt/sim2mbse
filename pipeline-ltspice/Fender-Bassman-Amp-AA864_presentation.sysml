package Fender_Bassman_Amp_AA864 {

  part BassmanAmp {

    port bassInput: AudioIn;
    port normalInput: AudioIn;
    port speakerOut: AudioOut;
    port ht1: PowerIn;
    port ht2: PowerIn;
    port ht3: PowerIn;
    port ht4: PowerIn;
    port biasControl: ControlIn;
    port gnd: Ground;

    attribute bass: Real;
    attribute treble: Real;
    attribute volume: Real;
    attribute brightSwitch: Boolean;
    attribute deepSwitch: Boolean;

  }

  interface AudioIn {
    flow in signal: Real;
  }

  interface AudioOut {
    flow out signal: Real;
  }

  interface PowerIn {
    flow in voltage: Real;
  }

  interface ControlIn {
    flow in control: Real;
  }

  interface Ground { }

  interface OtherPort { }
}
