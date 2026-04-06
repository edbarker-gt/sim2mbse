package Fender_Bassman_Amp_AA864 {

  part def AudioIn {}
  part def AudioOut {}
  part def PowerIn {}
  part def ControlIn {}
  part def Ground {}
  part def OtherPort {}

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
}
