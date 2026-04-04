package simple_example {
  private import ScalarValues::*;
  private import ISQ::*;
  private import SI::*;

  doc /*
    Flattened presentation-mode SysML v2-style model generated from
    baseline Nastran exchange JSON.
  */

  part simple_example {

    part solverContext {
      attribute name : String = "NASTRAN";
      attribute version : String = "unknown";
      attribute sol : Integer = 0;
    }

    part structuralSummary {
      attribute nodeCount : Integer = 20;
      attribute elementCountsByType : String = "CBAR=10, CBEAM=2, CBUSH=1, CQUAD4=4";
    }

    part material_1 {
      attribute mid : Integer = 1;
      attribute type : String = "MAT1";
    }

    part subcase_1 {
      attribute id : Integer = 1;
      attribute label : String = "SUBCASE_1";
      attribute analysisType : String = "";
      attribute spc : String = "";
      attribute load : String = "1";
    }

    part subcase_2 {
      attribute id : Integer = 2;
      attribute label : String = "SUBCASE_2";
      attribute analysisType : String = "";
      attribute spc : String = "";
      attribute load : String = "2";
    }

    part subcase_3 {
      attribute id : Integer = 3;
      attribute label : String = "SUBCASE_3";
      attribute analysisType : String = "";
      attribute spc : String = "";
      attribute load : String = "3";
    }

    part provenance {
      attribute sourceFiles : String = "simple-example.bdf";
      attribute timestamp : String = "2026-04-03T21:32:37+00:00";
    }

  }
}
