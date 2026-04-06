package Radar_Array_Antenna {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    Electromagnetics simulation JSON.
  */

  part Radar_Array_Antenna {

    part solverContext {
      attribute name : ScalarValues::String = "HFSS";
      attribute version : ScalarValues::String = "HFSS";
      attribute method : ScalarValues::String = "FEM";
      attribute frequencyRange : ScalarValues::String = "";
    }

    part copper {
      attribute id : ScalarValues::String = "copper";
      attribute type : ScalarValues::String = "conductor";
      attribute properties : ScalarValues::String = "";
    }

    part vacuum {
      attribute id : ScalarValues::String = "vacuum";
      attribute type : ScalarValues::String = "dielectric";
      attribute properties : ScalarValues::String = "";
    }

    part provenance {
      attribute sourceFiles : ScalarValues::String = "Radar-Array-Antenna.hfss";
      attribute timestamp : ScalarValues::String = "2026-04-05T14:08:19+00:00";
    }

  }
}
