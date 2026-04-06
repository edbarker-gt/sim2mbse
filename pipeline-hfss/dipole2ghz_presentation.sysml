package dipole2ghz {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    Electromagnetics simulation JSON.
  */

  part dipole2ghz {

    part solverContext {
      attribute name : String = "HFSS";
      attribute version : String = "ElectronicsDesktopStudent";
      attribute method : String = "FEM";
      attribute frequencyRange : String = "";
    }

    part air {
      attribute id : String = "air";
      attribute type : String = "dielectric";
      attribute properties : String = "";
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
      attribute sourceFiles : String = "dipole2ghz.aedt";
      attribute timestamp : String = "2026-04-05T14:18:12+00:00";
    }

  }
}
