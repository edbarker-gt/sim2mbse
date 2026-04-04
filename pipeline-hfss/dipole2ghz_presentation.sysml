package dipole2ghz {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    HFSS exchange JSON.
  */

  part dipole2ghz {

    part solverContext {
      attribute name : String = "HFSS";
      attribute family : String = "Electromagnetics";
      attribute product : String = "ElectronicsDesktopStudent";
      attribute designCount : Integer = 0;
    }

    part air {
      attribute name : String = "air";
    }

    part copper {
      attribute name : String = "copper";
    }

    part vacuum {
      attribute name : String = "vacuum";
    }

    part provenance {
      attribute sourceFiles : String = "dipole2ghz.aedt";
      attribute sourceFileName : String = "dipole2ghz.aedt";
      attribute sourceFileStem : String = "dipole2ghz";
      attribute timestamp : String = "2026-04-04T02:42:28+00:00";
    }

  }
}
