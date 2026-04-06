package dipole2ghz {

  doc /*
    Deterministic SysML v2-style model generated from
    Electromagnetics simulation JSON.
  */

  part def SolverContext {
    attribute name : String;
    attribute version : String;
    attribute method : String;
    attribute frequencyRange : String;
  }

  part def MaterialSummary {
    attribute id : String;
    attribute type : String;
    attribute properties : String;
  }

  part def PortSummary {
    attribute id : String;
    attribute type : String;
    attribute location : String;
    attribute impedance : String;
  }

  part def BoundarySummary {
    attribute id : String;
    attribute type : String;
    attribute appliesTo : String;
  }

  part def ProvenanceRecord {
    attribute sourceFiles : String;
    attribute timestamp : String;
  }

  part solverContext : SolverContext {
    name = "HFSS";
    version = "ElectronicsDesktopStudent";
    method = "FEM";
    frequencyRange = "";
  }

  part air : MaterialSummary {
    id = "air";
    type = "dielectric";
    properties = "";
  }

  part copper : MaterialSummary {
    id = "copper";
    type = "conductor";
    properties = "";
  }

  part vacuum : MaterialSummary {
    id = "vacuum";
    type = "dielectric";
    properties = "";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "dipole2ghz.aedt";
    timestamp = "2026-04-05T14:18:12+00:00";
  }

}
