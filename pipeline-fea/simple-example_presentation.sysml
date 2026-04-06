package simple_example {
  private import ScalarValues::*;

  part simple_example {

    part solverContext {
      attribute name : ScalarValues::String = "NASTRAN";
      attribute version : ScalarValues::String = "unknown";
      attribute sol : ScalarValues::Integer = 0;
    }

    part structuralSummary {
      attribute nodeCount : ScalarValues::Integer = 20;
      attribute elementCountsByType : ScalarValues::String = "CBAR=10, CBEAM=2, CBUSH=1, CQUAD4=4";
    }

    part material_1 {
      attribute mid : ScalarValues::Integer = 1;
      attribute type : ScalarValues::String = "MAT1";
    }

    part subcase_1 {
      attribute id : ScalarValues::Integer = 1;
      attribute label : ScalarValues::String = "SUBCASE_1";
      attribute analysisType : ScalarValues::String = "";
      attribute spc : ScalarValues::String = "";
      attribute load : ScalarValues::String = "1";
    }

    part subcase_2 {
      attribute id : ScalarValues::Integer = 2;
      attribute label : ScalarValues::String = "SUBCASE_2";
      attribute analysisType : ScalarValues::String = "";
      attribute spc : ScalarValues::String = "";
      attribute load : ScalarValues::String = "2";
    }

    part subcase_3 {
      attribute id : ScalarValues::Integer = 3;
      attribute label : ScalarValues::String = "SUBCASE_3";
      attribute analysisType : ScalarValues::String = "";
      attribute spc : ScalarValues::String = "";
      attribute load : ScalarValues::String = "3";
    }

    part provenance {
      attribute sourceFiles : ScalarValues::String = "simple-example.bdf";
      attribute timestamp : ScalarValues::String = "2026-04-03T21:32:37+00:00";
    }

  }
}
