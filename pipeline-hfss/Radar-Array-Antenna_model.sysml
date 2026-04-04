package Radar_Array_Antenna {

  doc /*
    Baseline deterministic SysML v2-style model generated from
    HFSS exchange JSON.
  */

  part def SolverContext {
    attribute name : String;
    attribute family : String;
    attribute product : String;
    attribute designCount : Integer;
  }

  part def DesignSummary {
    attribute designName : String;
    attribute solutionType : String;
    attribute globalMaterialEnvironment : String;
    attribute portImpedanceGlobal : String;
    attribute boundaryNames : String;
    attribute excitationNames : String;
    attribute setupNames : String;
  }

  part def MaterialSummary {
    attribute name : String;
  }

  part def ProvenanceRecord {
    attribute sourceFiles : String;
    attribute sourceFileName : String;
    attribute sourceFileStem : String;
    attribute timestamp : String;
  }

  part solverContext : SolverContext {
    name = "HFSS";
    family = "Electromagnetics";
    product = "HFSS";
    designCount = 0;
  }

  part copper : MaterialSummary {
    name = "copper";
  }

  part vacuum : MaterialSummary {
    name = "vacuum";
  }

  part provenance : ProvenanceRecord {
    sourceFiles = "Radar-Array-Antenna.hfss";
    sourceFileName = "Radar-Array-Antenna.hfss";
    sourceFileStem = "Radar-Array-Antenna";
    timestamp = "2026-04-04T02:45:14+00:00";
  }

}
