package Yagi_Uda {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    HFSS exchange JSON.
  */

  part Yagi_Uda {

    part solverContext {
      attribute name : String = "HFSS";
      attribute family : String = "Electromagnetics";
      attribute product : String = "HFSS";
      attribute designCount : Integer = 0;
    }

    part aluminum {
      attribute name : String = "aluminum";
    }

    part vacuum {
      attribute name : String = "vacuum";
    }

    part provenance {
      attribute sourceFiles : String = "Yagi_Uda.hfss";
      attribute sourceFileName : String = "Yagi_Uda.hfss";
      attribute sourceFileStem : String = "Yagi_Uda";
      attribute timestamp : String = "2026-04-04T02:42:28+00:00";
    }

  }
}
