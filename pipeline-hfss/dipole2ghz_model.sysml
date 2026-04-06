package dipole2ghz {

  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Deterministic SysML v2-style model generated from
    Electromagnetics simulation JSON.
  */

  part def SolverContext {
    attribute name : ScalarValues::String;
    attribute version : ScalarValues::String;
    attribute method : ScalarValues::String;
    attribute frequencyRange : ScalarValues::String;
  }

  part def MaterialSummary {
    attribute id : ScalarValues::String;
    attribute type : ScalarValues::String;
    attribute properties : ScalarValues::String;
  }

  part def PortSummary {
    attribute id : ScalarValues::String;
    attribute type : ScalarValues::String;
    attribute location : ScalarValues::String;
    attribute impedance : ScalarValues::String;
  }

  part def BoundarySummary {
    attribute id : ScalarValues::String;
    attribute type : ScalarValues::String;
    attribute appliesTo : ScalarValues::String;
  }

  part def ProvenanceRecord {
    attribute sourceFiles : ScalarValues::String;
    attribute timestamp : ScalarValues::String;
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
