# convert_study.py
# Template for HeuDiConv (Intro to BIDS, Brainhack DC 2020)
# Last edited by Shawn Rhoads 12/10/2020

import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    allowed template fields - follow python string module:
    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w_high_res = create_key('sub-{subject}/anat/sub-{subject}_acq-highres_T1w')

    localizer_01 = create_key('sub-{subject}/func/sub-{subject}_task-localizer_run-01_bold')
    localizer_02 = create_key('sub-{subject}/func/sub-{subject}_task-localizer_run-02_bold')
    localizer_03 = create_key('sub-{subject}/func/sub-{subject}_task-localizer_run-03_bold')

    phase = create_key('sub-{subject}/fmap/sub-{subject}_run-01_phasediff')
    mag = create_key('sub-{subject}/fmap/sub-{subject}_run-01_magnitude')

    info = {
            t1w_high_res: [],

            localizer_01: [],
            localizer_02: [],
            localizer_03: [],

            phase : [],
            mag  : []
            }

    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:
        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """

        if (s.dim3 == 176) and (s.dim4 == 1) and ('MPRAGE' in s.protocol_name):
            info[t1w_high_res] = [s.series_id]

        if (s.dim3 == 46) and (s.dim4 == 241) and ('localizer_01' in s.protocol_name):
            info[localizer_01] = [s.series_id]
        if (s.dim3 == 46) and (s.dim4 == 241) and ('localizer_02' in s.protocol_name):
            info[localizer_02] = [s.series_id]
        if (s.dim3 == 46) and (s.dim4 == 241) and ('localizer_03' in s.protocol_name):
            info[localizer_03] = [s.series_id]

        if (s.dim2 == 68) and (s.dim3 == 92) and ('gre_field_mapping' in s.protocol_name):
            info[mag] = [s.series_id]
        if (s.dim2 == 68) and (s.dim3 == 46) and ('gre_field_mapping' in s.protocol_name):
            info[phase] = [s.series_id]

    return info
