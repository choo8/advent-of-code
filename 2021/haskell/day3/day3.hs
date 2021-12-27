#!/usr/bin/env cabal
{- cabal:
       build-depends: base ^>=4.14.3.0, text, mtl
-}

module Main where

import Data.Char
import Control.Monad.State

type BinaryReport = [[Int]]

main :: IO ()
main = do
    contents <- getContents
    putStrLn $ "Part 1: " ++ (show $ part1 contents) ++ " Part 2: " ++ (show $ part2 contents)

processReport :: String -> BinaryReport
processReport xs = map (map digitToInt) $ lines xs

binaryAddition :: [Int] -> [Int] -> [Int]
binaryAddition (x:xs) (y:ys) = (x + y) : (binaryAddition xs ys)
binaryAddition _ _ = []

sumBinary :: BinaryReport -> [Int]
sumBinary xs = foldr1 binaryAddition xs

invertBinary :: [Int] -> [Int]
invertBinary (x:xs) =
    case x of
        0 -> 1 : (invertBinary xs)
        1 -> 0 : (invertBinary xs)
invertBinary [] = []

binaryToDecimal :: [Int] -> Int
binaryToDecimal (x:xs) = 
    case x of
        0 -> binaryToDecimal xs
        1 -> (2 ^ (length xs)) + (binaryToDecimal xs)
binaryToDecimal [] = 0

gammaRate :: BinaryReport -> [Int]
gammaRate xs = 
    let binarySum = sumBinary xs
        numNumbers = length xs
    in (map (\x -> if (quot numNumbers 2) < x then 1 else 0) binarySum)

part1 :: String -> Int
part1 xs =
    let gammaBinary = gammaRate $ processReport xs
        epsilonBinary = invertBinary gammaBinary
    in (binaryToDecimal gammaBinary) * (binaryToDecimal epsilonBinary)

mostCommonValue :: BinaryReport -> Int -> Int
mostCommonValue xs n =
    let binarySum = sumBinary xs
        element = binarySum !! n
        numNumbers = length xs
    in 
        if element >= ceiling ((fromIntegral numNumbers) / 2.0)
            then 1
            else 0

leastCommonValue :: BinaryReport -> Int -> Int
leastCommonValue xs n =
    case mostCommonValue xs n of
        0 -> 1
        1 -> 0

filterByValue :: BinaryReport -> Int -> Int -> BinaryReport
filterByValue xs n val = filter (\x -> if (x !! n) == val then True else False) xs

filterBinaryReport :: [Int] -> (BinaryReport -> Int -> Int) -> State BinaryReport [Int]
filterBinaryReport [] _ = do
    report <- get
    return (report !! 0)
filterBinaryReport (x:xs) f = do
    report <- get
    if (length report) == 1
        then do 
            return (report !! 0)
        else do
            put (filterByValue report x (f report x))
            filterBinaryReport xs f

part2 :: String -> Int
part2 xs =
    let report = processReport xs
        numBits = length (report !! 0)
        oxygenBinary = evalState (filterBinaryReport [0 .. (numBits - 1)] mostCommonValue) report
        co2Binary = evalState (filterBinaryReport [0 .. (numBits - 1)] leastCommonValue) report
    in (binaryToDecimal oxygenBinary) * (binaryToDecimal co2Binary)