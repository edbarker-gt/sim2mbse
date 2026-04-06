package test {
  private import ScalarValues::*;

  part test {

    part solverContext {
      attribute name : ScalarValues::String = "NASTRAN";
      attribute version : ScalarValues::String = "unknown";
      attribute sol : ScalarValues::Integer = 101;
    }

    part structuralSummary {
      attribute nodeCount : ScalarValues::Integer = 22;
      attribute elementCountsByType : ScalarValues::String = "CQUAD4=10";
    }

    part subcase_1 {
      attribute id : ScalarValues::Integer = 1;
      attribute label : ScalarValues::String = "SUBCASE_1";
      attribute analysisType : ScalarValues::String = "LinearStatic";
      attribute spc : ScalarValues::String = "2";
      attribute load : ScalarValues::String = "2";
    }

    part provenance {
      attribute sourceFiles : ScalarValues::String = "test.bdf";
      attribute timestamp : ScalarValues::String = "2026-04-03T21:32:37+00:00";
    }

  }
}
