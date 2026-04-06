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
      attribute name : String = "HFSS";
      attribute version : String = "HFSS";
      attribute method : String = "FEM";
      attribute frequencyRange : String = "";
    }

    part aluminum {
      attribute id : String = "aluminum";
      attribute type : String = "conductor";
      attribute properties : String = "";
    }

    part vacuum {
      attribute id : String = "vacuum";
      attribute type : String = "dielectric";
      attribute properties : String = "";
    }

    part provenance {
      attribute sourceFiles : String = "Yagi_Uda.hfss";
      attribute timestamp : String = "2026-04-05T14:18:07+00:00";
    }

  }
}
