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
      attribute name : String = "HFSS";
      attribute version : String = "HFSS";
      attribute method : String = "FEM";
      attribute frequencyRange : String = "";
    }

    part copper {
      attribute id : String = "copper";
      attribute type : String = "conductor";
      attribute properties : String = "";
    }

    part vacuum {
      attribute id : String = "vacuum";
      attribute type : String = "dielectric";
      attribute properties : String = "";
    }

    part provenance {
      attribute sourceFiles : String = "Radar-Array-Antenna.hfss";
      attribute timestamp : String = "2026-04-05T14:08:19+00:00";
    }

  }
}
