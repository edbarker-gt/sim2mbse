package Yagi_Uda {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    Electromagnetics simulation JSON.
  */

  part Yagi_Uda {

    part solverContext {
      attribute name : ScalarValues::String = "HFSS";
      attribute version : ScalarValues::String = "HFSS";
      attribute method : ScalarValues::String = "FEM";
      attribute frequencyRange : ScalarValues::String = "";
    }

    part aluminum {
      attribute id : ScalarValues::String = "aluminum";
      attribute type : ScalarValues::String = "conductor";
      attribute properties : ScalarValues::String = "";
    }

    part vacuum {
      attribute id : ScalarValues::String = "vacuum";
      attribute type : ScalarValues::String = "dielectric";
      attribute properties : ScalarValues::String = "";
    }

    part provenance {
      attribute sourceFiles : ScalarValues::String = "Yagi_Uda.hfss";
      attribute timestamp : ScalarValues::String = "2026-04-05T14:18:07+00:00";
    }

  }
}
