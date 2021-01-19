<?php
    // Ititial data
    $request = json_decode(file_get_contents('php://input'), true);
    $I2R = json_decode(file_get_contents("Id2Row.json"), true);
    $hash = json_decode(file_get_contents("hash.json"), true);


    // itemCF prediction
    function Recommend($userData, $W, $K) {
        $rank = array();
        foreach ($userData as $work => $rate) {
            arsort($W[$work]);
            foreach (array_slice($W[$work], 0, $K, true) as $j => $wj) {
                if (in_array($j, array_keys($userData)))    continue;
                if (!array_key_exists($j, $rank)) $rank[$j] = 0;
                $rank[$j] += $rate * $wj;
            }
        }

        arsort($rank);
        return $rank;
    }



    // filter the recoreded data
    $userData = array();
    foreach($request as $work => $rate)
        if (array_key_exists($work, $I2R))
            $userData[$work] = $rate;

    // load asso list
    $W = array();
    foreach (array_keys($userData) as $work) {
        $line = $I2R[$work];
        $prv = 0;
        for ($i = 0; $i < count($hash); $i++) {
            $cur = $hash[$i];
            if ($prv < $line && $line <= $cur) break;
            $prv = $hash[$i];
        }
        $fp = new SplFileObject("dataBase/".$cur.".txt");
        $fp->seek($line - $prv - 1);
        $W[$work] = (array)json_decode($fp->current(), true)[$work];
    }

    // run prediction
    $pred = Recommend($userData, $W, 15);
    $otp = array();
    foreach(array_keys($pred) as $work)
        $otp[] = $work;
    // var_dump(array_slice($pred, 0, 25, true));
    echo json_encode(array_slice($otp, 0, 25, true));
?>