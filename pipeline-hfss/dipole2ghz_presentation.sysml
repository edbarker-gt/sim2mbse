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
      attribute name : ScalarValues::String = "HFSS";
      attribute version : ScalarValues::String = "ElectronicsDesktopStudent";
      attribute method : ScalarValues::String = "FEM";
      attribute frequencyRange : ScalarValues::String = "";
    }

    part air {
      attribute id : ScalarValues::String = "air";
      attribute type : ScalarValues::String = "dielectric";
      attribute properties : ScalarValues::String = "";
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
      attribute sourceFiles : ScalarValues::String = "dipole2ghz.aedt";
      attribute timestamp : ScalarValues::String = "2026-04-05T14:18:12+00:00";
    }

  }
}
