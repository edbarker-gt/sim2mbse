package Yagi_Uda {

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
    version = "HFSS";
    method = "FEM";
    frequencyRange = "";
  }

  part aluminum : MaterialSummary {
    id = "aluminum";
    type = "conductor";
    properties = "";
  }

  part vacuum : MaterialSummary {
    id = "vacuum";
    type = "dielectric";
    properties = "";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "Yagi_Uda.hfss";
    timestamp = "2026-04-05T14:18:07+00:00";
  }

}
