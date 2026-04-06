package Yagi_Uda {

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
