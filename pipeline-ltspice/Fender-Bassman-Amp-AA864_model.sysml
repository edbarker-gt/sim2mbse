package Fender_Bassman_Amp_AA864 {

  private import ScalarValues::*;

  part def AudioIn {}
  part def AudioOut {}
  part def PowerIn {}
  part def ControlIn {}
  part def Ground {}
  part def OtherPort {}

  part BassmanAmp {

    part bassInput : AudioIn;
    part normalInput : AudioIn;
    part speakerOut : AudioOut;
    part ht1 : PowerIn;
    part ht2 : PowerIn;
    part ht3 : PowerIn;
    part ht4 : PowerIn;
    part biasControl : ControlIn;
    part gnd : Ground;

    attribute bass: ScalarValues::Real;
    attribute treble: ScalarValues::Real;
    attribute volume: ScalarValues::Real;
    attribute brightSwitch: ScalarValues::Boolean;
    attribute deepSwitch: ScalarValues::Boolean;

  }
}
