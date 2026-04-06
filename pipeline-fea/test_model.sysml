package test {

  private import ScalarValues::*;

  doc /*
    Baseline deterministic SysML v2-style model generated from
    Nastran exchange JSON.
  */

  part def SolverContext {
    attribute name : ScalarValues::String;
    attribute version : ScalarValues::String;
    attribute sol : ScalarValues::Integer;
  }

  part def StructuralSummary {
    attribute nodeCount : ScalarValues::Integer;
    attribute elementCountsByType : ScalarValues::String;
  }

  part def MaterialSummary {
    attribute mid : ScalarValues::Integer;
    attribute type : ScalarValues::String;
  }

  part def AnalysisCase {
    attribute id : ScalarValues::Integer;
    attribute label : ScalarValues::String;
    attribute analysisType : ScalarValues::String;
    attribute spc : ScalarValues::String;
    attribute load : ScalarValues::String;
  }

  part def ProvenanceRecord {
    attribute sourceFiles : ScalarValues::String;
    attribute timestamp : ScalarValues::String;
  }

  part solverContext : SolverContext {
    name = "NASTRAN";
    version = "unknown";
    sol = 101;
  }

  part structuralSummary : StructuralSummary {
    nodeCount = 22;
    elementCountsByType = "CQUAD4=10";
  }

  part subcase_1 : AnalysisCase {
    id = 1;
    label = "SUBCASE_1";
    analysisType = "LinearStatic";
    spc = "2";
    load = "2";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "test.bdf";
    timestamp = "2026-04-03T21:32:37+00:00";
  }

}
