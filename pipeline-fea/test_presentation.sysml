package test {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    baseline Nastran exchange JSON.
  */

  part test {

    part solverContext {
      attribute name : String = "NASTRAN";
      attribute version : String = "unknown";
      attribute sol : Integer = 101;
    }

    part structuralSummary {
      attribute nodeCount : Integer = 22;
      attribute elementCountsByType : String = "CQUAD4=10";
    }

    part subcase_1 {
      attribute id : Integer = 1;
      attribute label : String = "SUBCASE_1";
      attribute analysisType : String = "LinearStatic";
      attribute spc : String = "2";
      attribute load : String = "2";
    }

    part provenance {
      attribute sourceFiles : String = "test.bdf";
      attribute timestamp : String = "2026-04-03T21:32:37+00:00";
    }

  }
}
