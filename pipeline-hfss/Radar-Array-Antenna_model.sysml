package Radar_Array_Antenna {

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
    sourceFiles = "Radar-Array-Antenna.hfss";
    timestamp = "2026-04-05T14:08:19+00:00";
  }

}
